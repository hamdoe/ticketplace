'use strict';

app.controller('registrationController', ['$scope', '$upload', 'Signature', 'Company',
    function($scope, $upload, Signature, Company) {
        $scope.company = {};
        $scope.idCheck = idCheck;
        $scope.openDaumPostcode = openDaumPostcode;
        $scope.files = {};
        $scope.upload = upload;
        $scope.waiting_upload = false;
        $scope.submit = submit;

        Signature.get(function(response){
            $scope.policy = response.policy;
            $scope.signature = response.signature;
            $scope.access_key = response.access_key;
          });

        function idCheck() {
            duplicateCheck.check(function(data) {
                if (data === true) {
                    $scope.company.duplicate = "이미 존재하는 아이디입니다.";
                    console.dir($scope.company.$error);
                } else {
                    $scope.company.duplicate = data;
                    console.dir($scope.company.$error);
                }
            }, $scope.company.id);
        }

        function openDaumPostcode(){
            new daum.Postcode({
                oncomplete : function(data) {
                    // 팝업에서 검색결과 항목을 클릭했을때 실행할 코드를 작성하는 부분.
                    // 우편번호와 주소 정보를 해당 필드에 넣고, 커서를 상세주소 필드로 이동한다.

                    $scope.company.postcode1 = data.postcode1;
                    $scope.company.postcode2 = data.postcode2;
                    $scope.company.address1 = data.address;
                    $scope.$apply();
                    //전체 주소에서 연결 번지 및 ()로 묶여 있는 부가정보를 제거하고자 할 경우,
                    //아래와 같은 정규식을 사용해도 된다. 정규식은 개발자의 목적에 맞게 수정해서 사용 가능하다.
                    //var addr = data.address.replace(/(\s|^)\(.+\)$|\S+~\S+/g, '');
                    //document.getElementById('addr').value = addr;

                    document.getElementById('addr2').focus();
                }
            }).open();
        }


        function upload(files, content, image_type){
            if(files && files.length){
                $scope.waiting_upload = true;
                var file = files[0];
                var now = new Date();
                var timestamp = ''+now.getFullYear()+'_'+(now.getMonth()+1)+'_'+now.getDate()+'_'+now.getHours()+'_'+now.getMinutes()+'_'+now.getSeconds();
                content[image_type] = image_type + '_' + timestamp+ '_' + file.name;
                $upload.upload({
                    url: 'https://ticketplace.s3.amazonaws.com/', //S3 upload url including bucket name
                    method: 'POST',
                    fields : {
                        key: 'uploads/' + content[image_type], // the key to store the file on S3, could be file name or customized
                        AWSAccessKeyId: $scope.access_key,
                        acl: 'public-read', // sets the access to the uploaded file in the bucket: private or public
                        policy: $scope.policy, // base64-encoded json policy (see article below)
                        signature: $scope.signature, // base64-encoded signature based on policy string (see article below)
                        "Content-Type": file.type != '' ? file.type : 'application/octet-stream' // content type of the file (NotEmpty)
                    },
                    file: file
                }).progress(function (evt) {
                    $scope.upload_percentage = 100 * evt.loaded / evt.total ;
                }).success(function(data, status, headers, config) {
                    $scope.waiting_upload = false;
                });
            }
        }

        function submit(){
            /* 전화번호에 하이픈(-) 없으면 하이픈 자동 입력 */
            if (/^\d{3}\d{2}\d{5}$/.test($scope.company.company_number)) {
                $scope.company.company_number = $scope.company.company_number.replace(/^(\d{3})(\d{3,4})(\d{4})$/, '$1-$2-$3')
            }
            if (/^\d{3}\d{3,4}\d{4}$/.test($scope.company.manager_phone)) {
                $scope.company.manager_phone = $scope.company.manager_phone.replace(/^(\d{3})(\d{3,4})(\d{4})$/, '$1-$2-$3')
            }
            if (/^\d{3}\d{3,4}\d{4}$/.test($scope.company.represent_phone)) {
                $scope.company.represent_phone = $scope.company.represent_phone.replace(/^(\d{3})(\d{3,4})(\d{4})$/, '$1-$2-$3')
            }
            /* invalid input에 포커스 */
            if($scope.companyForm.$invalid){
                focus_first_invalid($scope.companyForm);
                return;
            }
            if(!$scope.agreed){
                companyForm['agreed'].focus();
                return;
            }
            if(!$scope.company.business_license){
                alert('사업자 등록증 사본을 업로드 해 주세요.')
                return;
            }
            if($scope.copy_info){
                $scope.company.manager_name = $scope.company.represent_name;
                $scope.company.manager_phone = $scope.company.represent_phone;
                $scope.company.manager_email = $scope.company.represent_email;
            }
            Company.create($scope.company, function(){
                alert('회원가입에 성공하셨습니다. 로그인 창으로 이동합니다.')
                window.location.href = 'http://admin.ticketplace.net';
            })
        }

        function focus_first_invalid(form){
            // set focus to first invalid form element
            // form : angular form object
            // assumes the existance of javascript form object: window[form.$name] (ex: register_form)
            var is_first_error = true;
            for (var field in form){
                if(field[0] == '$'){
                    // ignore form's attributes such as $pristine and $valid
                    continue;
                }
                if(form[field].$invalid){
                    if( is_first_error ){
                        window[form.$name][field].focus();
                        is_first_error = false;
                    }
                }
            }
        }
    }]);


app.directive('equals', function() {
    return {
        restrict : 'A', // only activate on element attribute
        require : '?ngModel', // get a hold of NgModelController
        link : function(scope, elem, attrs, ngModel) {
            if (!ngModel)
                return; // do nothing if no ng-model

            // watch own value and re-validate on change
            scope.$watch(attrs.ngModel, function() {
                validate();
            });

            // observe the other value and re-validate on change
            attrs.$observe('equals', function(val) {
                validate();
            });

            var validate = function() {
                // values
                var val1 = ngModel.$viewValue;
                var val2 = attrs.equals;

                // set validity
                ngModel.$setValidity('equals', !val1 || !val2
                || val1 === val2);
            };
        }
    }
});

app.directive('uniqueId', [
    '$http',
    function($http) {
        return {
            restrict : 'A',
            require : '?ngModel',
            link : function(scope, element, attrs, ctrl) {
                scope.$watch(attrs.ngModel, function() {
                    $http({
                        method : 'GET',
                        url : 'api/company?q={"filters":[{"name":"id", "op":"==", "val":"'+ ctrl.$viewValue +'"}]}'

                    }).success(
                        function(data, status, headers, cfg) {
                            if (data.num_results === 0) {
                                ctrl.$setValidity('unique',
                                    true);
                            } else {
                                ctrl.$setValidity('unique',
                                    false);
                            }
                        }).error(
                        function(data, status, headers, cfg) {
                            ctrl.$setValidity('unique', false);
                        });
                });
            }
        };
    } ]);

app.factory('duplicateCheck', function($http) {
    return {
        check : function(callback, id) {
            return true
        }
    }
});