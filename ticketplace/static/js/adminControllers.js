'use strict';

var app = angular.module('adminApp');

/*

 Sidebar에서 Badge에 새로운 알람을 표시해주는 기능을 위해 Company에 대한 정보가 필요하다.

 */
app.controller('adminSidebarController', ['$rootScope', '$scope', '$location', 'Company',
    function ($rootScope, $scope, $location, Company) {
        $scope.is_active = function (location) {
            // nav에서 현재 페이지 표시 용
            return location === $location.path();
        };

        $scope.get_class = function (location) {
            // ng-class용
            if ($scope.is_active(location)) {
                return 'active';
            }
            else {
                return '';
            }
        };

        Company.get_current(function ($response) {
            $rootScope.company = $response
        });
    }]);

/*

 registerContentController

 컨텐츠 판매 신청과 관련된 컨트롤러.

 */
app.controller('registerContentController', ['$scope', '$upload', '$location', 'Content', 'Signature',
    function ($scope, $upload, $location, Content, Signature) {
        $scope.submit = submit_content;
        $scope.upload = upload;
        $scope.waiting_upload = false;
        $scope.openDaumPostcode = openDaumPostCode;

        function submit_content() {
            /* 전화번호에 하이픈(-) 없으면 하이픈 자동 입력 */
            if (/^\d{3}\d{3,4}\d{4}$/.test($scope.content.manager_phone)) {
                $scope.content.manager_phone = $scope.content.manager_phone.replace(/^(\d{3})(\d{3,4})(\d{4})$/, '$1-$2-$3')
            }
            if (/^\d{2,3}\d{3,4}\d{4}$/.test($scope.content.inquire_number)) {
                $scope.content.inquire_number = $scope.content.inquire_number.replace(/^(\d{3})(\d{3,4})(\d{4})$/, '$1-$2-$3')
            }
            if ($scope.register_form.$invalid){
                focus_first_invalid($scope.register_form);
                return;
            }
            Content.create($scope.content, function success(response) {
                alert('컨텐츠 등록이 완료되었습니다.');
                $location.path('/product/detail/' + response.content_id);
            }, function error(e) {
                console.log(e);
                alert('에러가 발생하여 등록에 실패하였습니다. 인터넷 환경을 확인하고 다시 시도해주세요.');
            });
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

        /*

         아마존 AWS에 업로드하는 관계로 코드가 복잡한 편.
         이전에 Wiki 암호학 문서를 뒤져가며 코드를 만들었던 것 같은데..
         코드의 의미가 궁금하다면 김민준에게 물어보시오.

         */
        function upload(files) {
            if (files && files.length) {
                $scope.waiting_upload = true;
                var file = files[0];
                var now = new Date();
                var timestamp = '' + now.getFullYear() + '_' + (now.getMonth() + 1) + '_' + now.getDate() + '_' + now.getHours() + '_' + now.getMinutes() + '_' + now.getSeconds();
                $scope.content.information_file = 'zip' + '_' + timestamp + '_' + file.name;
                $upload.upload({
                    url: 'https://ticketplace.s3.amazonaws.com/', //S3 upload url including bucket name
                    method: 'POST',
                    fields: {
                        key: 'uploads/' + $scope.content.information_file, // the key to store the file on S3, could be file name or customized
                        AWSAccessKeyId: $scope.access_key,
                        acl: 'public-read', // sets the access to the uploaded file in the bucket: private or public
                        policy: $scope.policy, // base64-encoded json policy (see article below)
                        signature: $scope.signature, // base64-encoded signature based on policy string (see article below)
                        "Content-Type": file.type != '' ? file.type : 'application/octet-stream' // content type of the file (NotEmpty)
                    },
                    file: file
                }).progress(function (evt) {
                    $scope.upload_percentage = 100 * evt.loaded / evt.total;
                }).success(function(data, status, headers, config) {
                    $scope.waiting_upload = false;
                });
            }
        }

        /*
         다음 우편번호 찾기 서비스
         */
        function openDaumPostCode() {
            new daum.Postcode({
                oncomplete: function (data) {
                    $scope.content.theater_postcode1 = data.postcode1;
                    $scope.content.theater_postcode2 = data.postcode2;
                    $scope.content.theater_address1 = data.address;
                    $scope.$apply();
                }
            }).open();
        }


        (function init() {
            /*

             입력 폼 초기화

             */
            $scope.content = {};
            $scope.content.company_id = current_user.company_id;
            $scope.content.status = 1;
            $scope.content.genre = 0;
            $scope.content.location = 0;
            $scope.content.actor_change = 0;
            $scope.content.landing_ad = 0;
        })();

        Signature.get(function (response) {
            $scope.policy = response.policy;
            $scope.signature = response.signature;
            $scope.access_key = response.access_key;
        });

        $scope.$watch('files', function () {
            $scope.upload($scope.files);
        });
    }]);


/*

 제작사 개인정보 수정

 */
app.controller('modifyCompanyController', ['$scope', '$rootScope', '$upload', '$location', 'Signature', 'Company',
    function ($scope, $rootScope, $upload, $location, Signature, Company) {
        Company.get({'company_id': current_user.company_id}, function($response){
            $rootScope.company = $response;
            $scope.company = {
                company_id: $rootScope.company.company_id,
                id: $rootScope.company.id,
                company_type: $rootScope.company.company_type,
                company_name: $rootScope.company.company_name,
                company_number: $rootScope.company.company_number,
                mail_order_number: $rootScope.company.mail_order_number,
                tax_type: $rootScope.company.tax_type,
                postcode1: $rootScope.company.postcode1,
                postcode2: $rootScope.company.postcode2,
                address1: $rootScope.company.address1,
                address2: $rootScope.company.address2,
                represent_name: $rootScope.company.represent_name,
                represent_phone: $rootScope.company.represent_phone,
                represent_email: $rootScope.company.represent_email,
                manager_name: $rootScope.company.manager_name,
                manager_phone: $rootScope.company.manager_phone,
                manager_email: $rootScope.company.manager_email,
                account_bank_code: $rootScope.company.account_bank_code,
                account_number: $rootScope.company.account_number,
                account_name: $rootScope.company.account_name
            };
        });
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

        function submit() {
            if($scope.form.$invalid){
                focus_first_invalid($scope.form);
                return;
            }
            if($scope.password){
                $scope.company.password = $scope.password;
            }
            if($scope.copy_info){
                $scope.company.manager_name = $scope.company.represent_name;
                $scope.company.manager_phone = $scope.company.represent_phone;
                $scope.company.manager_email = $scope.company.represent_email;
            }
            $scope.waiting = true;
            Company.update($scope.company, function(success){
                alert('회원정보가 수정되었습니다.')
                $scope.waiting = false;
                $location.path('/');
            });
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
                    console.log('' + form[field] + ' is invalid');
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
/*

 콘텐츠 페이지

 */

app.controller('productController', ['$scope', '$routeParams', '$location', '$modal', 'Content', 'Company', 'Reservation',
    function ($scope, $routeParams, $location, $modal, Content, Company, Reservation) {
        $scope.search_detail = search_detail;
        $scope.status = {'pending': [0, 1], 'on_sale': [2], 'sold': [3]}[$routeParams['status']];
        $scope.page_subtitle = {
            'all': '전체 내역',
            'pending': '등록중',
            'on_sale': '판매중',
            'sold': '판매종료'
        }[$routeParams['status']];
        $scope.get_total_capacity = get_total_capacity;
        $scope.load_contents = load_contents;
        $scope.waiting = true;
        $scope.register_content = register_content;
        $scope.cancel_register_content = cancel_register_content;
        $scope.close_content = close_content;
        $scope.delete_content = delete_content;
        $scope.open_modal_resolved = open_modal_resolved;
        $scope.modify_content = modify_content;

        load_contents();

        function load_contents() {
            var query = {};
            var q = {q: query};
            query.filters = [];
            var filter = function (name, op, val) {
                return {name: name, op: op, val: val}
            }
            query.filters.push(filter('company_id', '==', current_user.company_id));
            if (typeof $scope.status !== 'undefined') {
                var status_filters = {or: []};
                for (var i = 0; i < $scope.status.length; i++) {
                    var status = $scope.status[i];
                    status_filters.or.push(filter('status', '==', status));
                }
                query.filters.push(status_filters);
            }
            Content.query(q, function ($response) {
                $scope.contents = $response.data.objects;
                $scope.waiting = false;
            });
        }

        function search_detail(content) {
            $location.path('/product/detail/' + content.content_id)
        }

        function get_total_capacity(content) {
            var total_capacity = 0;
            for (var i in content.content_time_list) {
                var content_time = content.content_time_list[i];
                total_capacity += content_time.assigned_capacity
            }
            return total_capacity;
        }

        function register_content(index) {
            var content = $scope.contents[index];
            if (content.status !== 0) {
                return
            }
            $scope.waiting = true;
            Content.update({content_id: content.content_id, status: 1});
            load_contents()
        }


        function cancel_register_content(index) {
            var content = $scope.contents[index];
            if (content.status !== 1) {
                return
            }
            $scope.waiting = true;
            Content.update({content_id: content.content_id, status: 0}, function () {
                load_contents()
            });
        }

        function close_content($event, content) {
            $event.preventDefault();
            $event.stopPropagation();
            if (content.status !== 2) {
                alert('이 콘텐츠는 마감할 수 없습니다.');
                return;
            }
            if (!confirm('이 공연을 마감하시겠습니까?')) return;

            $scope.waiting = true;
            Content.update({content_id: content.content_id, status: 3}, function () {
                load_contents();
            });
        }

        function delete_content($event, content) {
            $event.preventDefault();
            $event.stopPropagation();
            if (!confirm('정말로 이 공연을 삭제하시겠습니까?\n(이 작업은 복구가 불가능합니다.)')) return;
            $scope.waiting = true;
            Content.delete({content_id: content.content_id}, function () {
                load_contents();
            }, function (error) {
                console.log(error);
                alert('삭제에 실패하였습니다. 하위 예약/공연시간 등을 모두 삭제하고 다시 시도해주세요.')
                $scope.waiting = false;
            })
        }

        function open_modal_resolved($event, content) {
            $event.preventDefault();
            $event.stopPropagation();
            var modalInstance = $modal.open({
                templateUrl: '/admin/modals/resolvedModal.html',
                controller: 'resolvedModalController',
                resolve: {
                    content: function () {
                        return content;
                    },
                    reservation: function () {
                        return {};
                    }
                }
            });
        }

        function modify_content($event, content) {
            $event.preventDefault();
            $event.stopPropagation();
        }
    }]);

/*

 콘텐츠 상세 페이지

 */
app.controller('productDetailController', ['$scope', '$routeParams', '$window', '$location', '$modal', 'ContentTime', 'Content', 'Reservation',
    function ($scope, $routeParams, $window, $location, $modal, ContentTime, Content, Reservation) {
        $scope.content_id = $routeParams.content_id;
        $scope.delete_time = delete_time;
        $scope.close_time = close_time;
        $scope.reopen_time = reopen_time;
        $scope.add_time = add_time;
        $scope.edit_capacity = edit_capacity;
        $scope.update_assigned_capacity = update_assigned_capacity;
        if ($routeParams['date']) {
            $scope.dt = new Date($routeParams['date'])
        }
        $scope.open_datepicker = open_datepicker;
        $scope.datepicker = {}; // datepicker.opened 용. primitive value일경우 오류가 난다.
        $scope.datepicker_format = 'yyyy년 MM월 dd일';
        $scope.dateoptions = {
            showWeeks:false
        };
        $scope.new_time = new Date(2000, 0, 0, 12);
        $scope.go_back = go_back_history;
        $scope.goto_reservation = goto_reservation;
        $scope.open_modal_resolved = open_modal_resolved;
        $scope.open_modal_external = open_modal_external;
        $scope.stop_event = function ($event) {
            $event.preventDefault();
            $event.stopPropagation();
        };

        load_content_times();


        function load_content_times() {
            Content.get({
                content_id: $scope.content_id
            }, function (response) {
                $scope.content = response.data;

                //컨텐츠 타임 일자별 정렬
                $scope.content_times = response.data.content_time_list.sort(function(a, b){
                    return new Date(a.date)- new Date(b.date);
                });
                $scope.waiting = false;
            });
        }


        function close_time($event, content_time) {
            $event.preventDefault();
            $event.stopPropagation();
            if (!confirm('이 타임을 마감하시겠습니까?')) return;
            $scope.waiting = true;
            ContentTime.update({content_time_id: content_time.content_time_id, status: 1}, function (success) {
                load_content_times();
            })
        }

        function reopen_time($event, content_time) {
            $event.preventDefault();
            $event.stopPropagation();
            if(!confirm('마감을 취소하시겠습니까?')) return;
            $scope.waiting = true;
            ContentTime.update({content_time_id: content_time.content_time_id, status: 0}, function (success) {
                load_content_times();
            })
        }

        function goto_reservation(content_time) {
            $location.path('/reservation/content_time/' + content_time.content_time_id)
        }

        function delete_time($event, content_time) {
            $event.preventDefault();
            $event.stopPropagation();
            if (!confirm('정말로 삭제하시겠습니까?\n(이 작업은 되돌릴 수 없습니다.)')) return;
            $scope.waiting = true;
            ContentTime.delete({content_time_id: content_time.content_time_id}, function (success) {
                load_content_times();
            }, function (error) {
                alert('삭제에 실패하였습니다. 하위 예약이 하나도 없는지 확인하시고 다시 시도해주세요.')
                $scope.waiting = false;
            })
        }

        function add_time(date, time) {
            if (!date) {
                alert('일자를 입력해주세요.');
                return
            }
            if (!time) {
                alert('시간을 입력해주세요.');
                return
            }
            $scope.waiting = true;
            // 타임존 주의
            var new_time = new Date(Date.UTC(date.getFullYear(), date.getMonth(), date.getDate(),
                time.getHours() - 9,
                time.getMinutes()));
            var new_content_time = {
                content_id: $scope.content.content_id,
                assigned_capacity: $scope.content.capacity,
                date: new_time,
                status: 0
            };
            ContentTime.create(new_content_time, function (success) {
                load_content_times();
            })
        }

        function open_datepicker($event) {
            $event.preventDefault();
            $event.stopPropagation();
            $scope.datepicker.opened = true;
        }

        function edit_capacity(content_time) {
            $scope.edit_assigned_capacity = true;
            $scope.new_assigned_capacity = content_time.assigned_capacity;
        }

        function update_assigned_capacity($index, new_assigned_capacity) {
            $scope.waiting = true;
            var content_time = $scope.content_times[$index];
            content_time.assigned_capacity = new_assigned_capacity;
            ContentTime.update({
                    content_time_id:content_time.content_time_id,
                    assigned_capacity:content_time.assigned_capacity
                }, function (success) {
                alert('좌석 수가 성공적으로 변경되었습니다.')
                load_content_times();
            })
        }

        function go_back_history() {
            $window.history.back();
        }

        function open_modal($index) {
            var modalInstance = $modal.open({
                templateUrl: 'myModalContent.html',
                controller: 'modalInstanceController',
                resolve: {
                    reservation: function () {
                        return $scope.reservations[$index];
                    }
                }
            });

            $scope.reservation = $scope.reservations[$index];

            modalInstance.result.then(function (reservation) {
                console.log(reservation);
            })
        }

        function open_modal_resolved() {
            var modalInstance = $modal.open({
                templateUrl: '/admin/modals/resolvedModal.html',
                controller: 'resolvedModalController',
                resolve: {
                    content: function () {
                        return $scope.content
                    }
                }
            });
        }

        function open_modal_external($event, content_time) {
            $event.preventDefault();
            $event.stopPropagation();
            var modalInstance = $modal.open({
                templateUrl: '/admin/modals/externalReservationModal.html',
                controller: 'externalReservationModalController',
                size: 'lg',
                resolve: {
                    content: function () {
                        return $scope.content;
                    },
                    content_time: function () {
                        return content_time;
                    }
                }
            }).result.then(function () {
                    alert('외부 예약이 등록되었습니다.');
                    load_content_times()
                })
        }

    }]);

app.controller('adminReservationPerContentTimeController', ['$scope', '$rootScope', '$routeParams', '$filter', '$modal', '$location', '$window',
    'Company', 'Content', 'ContentTime', 'Reservation', 'SMS',
    function ($scope, $rootScope, $routeParams, $filter, $modal, $location, $window,
              Company, Content, ContentTime, Reservation, SMS) {
        $scope.close_time = close_time;
        $scope.reopen_time = reopen_time;
        $scope.approve = approve;
        $scope.reject = reject;
        $scope.set_watched = set_watched;
        $scope.delete = delete_reservation;
        $scope.delete_time = delete_time;
        $scope.open_datepicker = open_datepicker;
        $scope.search_reservation = search_reservation;
        $scope.change_capacity = change_capacity;
        $scope.go_back = go_back_history;

        $scope.datepicker = {}; // datepicker.opened 용. primitive value일경우 오류가 난다.
        $scope.datepicker_format = 'yyyy년 MM월 dd일';
        $scope.dateoptions = {
            showWeeks:false
        };
        $scope.waiting = true;
        $scope.is_new = $routeParams['new']==='new';
        $scope.open_modal_external = open_modal_external;

        reload();

        if ($routeParams['date']) {
            $scope.dt = new Date($routeParams['date'])
        }

        function reload() {
            load_company();
            load_reservation();
        }

        function load_company() {
            Company.get_current(function(response){
                $rootScope.company = response;
            });
        }

        function load_reservation() {
            // Using jquery with angular is an anti pattern
            // but since we are migrating from angular to jquery, it's okay
            $.get('/api/admin/reservation',
                {'new': $scope.is_new,
                'content_time_id': $routeParams['content_time_id']},
                function (response) {
                    $scope.reservations = response.objects;
                    for(var i= 0; i<$scope.reservations.length; i++){ // parse date
                        $scope.reservations[i].content_time.date = Date.parse($scope.reservations[i].content_time.date)
                    }
                    $scope.reservations_filtered = $scope.reservations;

                    if ($routeParams['content_time_id']) {
                        ContentTime.query({content_time_id: $routeParams['content_time_id']}, function (response) {
                            $scope.content_time = response;
                            $scope.content = response.content;
                        })
                    }
                    if ($routeParams['date']) {
                        search_reservation($scope.dt)
                    }
                    $scope.$apply();
                    $scope.waiting = false;
                }
            )
        }

        function go_back_history() {
            $window.history.back();
        }

        function close_time(content_time) {
            $scope.waiting = true;
            ContentTime.update({content_time_id: content_time.content_time_id, status: 1}, function (success) {
                reload();
            })
        }

        function reopen_time(content_time) {
            $scope.waiting = true;
            ContentTime.update({content_time_id: content_time.content_time_id, status: 0}, function (success) {
                reload();
            })
        }

        function delete_time(content_time) {
            if (!confirm('정말로 삭제하시겠습니까?\n(이 작업은 되돌릴 수 없습니다.)')) return;
            $scope.waiting = true;
            ContentTime.delete({content_time_id: content_time.content_time_id}, function (success) {
                alert('성공적으로 삭제하였습니다. 콘텐츠 관리 상세 페이지로 돌아갑니다.');
                $location.path('/product/detail/' + content_time.content_id);
            }, function (error) {
                alert('삭제에 실패하였습니다. 하위 예약이 하나도 없는지 확인하시고 다시 시도해주세요.');
                $scope.waiting = false;
            })
        }

        function approve(reservation) { // can't get reservation directly as a parameter because we need to update $scope
            if (reservation.status != 1) {
                $scope.waiting = true;
                Reservation.update({reservation_id: reservation.reservation_id}, {status: 1}, function ($response) {
                    SMS.send({
                        phone_number: reservation.manager_phone,
                        content: '[ 에듀티켓-예약 완료 ]\n' +
                                 '입장안내입니다. 공연장 입구에서 본 문자내역을 보여주세요.\n' +
                                 '\n' +
                                 moment(reservation.content_time.date).format('M월 D일') + reservation.organization_name + ' ' + reservation.manager_name + '선생님 예약내역입니다.\n' +
                                 reservation.content.name + ' | ' + reservation.charged + '명 예약 | 인솔자 ' + reservation.chargeless + '명 무료\n' +
                                 '\n' +
                                 '관람 후 결제청구서가 발송됩니다.\n'
                   });
                    reload();
                    //send_email($scope.reservations[i]);
                    //send_sms($scope.reservations[i]);
                });
            }
        }

        function reject(reservation) { // can't get reservation directly as a parameter because we need to update $scope
            if (reservation.status != 1) {
                $scope.waiting = true;
                Reservation.update({reservation_id: reservation.reservation_id}, {status: 6}, function ($response) {
                    reload();
                    //send_email($scope.reservations[i]);
                    //send_sms($scope.reservations[i]);
                });
            }
        }

        function set_watched(reservation) {
            /* 관람 확인 시 실제로 본 인원 수 입력 */
            var modalInstance = $modal.open({
                templateUrl: '/admin/modals/watchedModal.html',
                controller: 'watchedModalController',
                size: 'lg',
                resolve: {
                    reservation: function () {
                        return reservation;
                    }
                }
            }).result.then(function () {
                    reload()
                })
        }

        function delete_reservation(reservation) {
            if(!confirm("정말로 삭제하시겠습니까?\n(이 작업은 되돌릴 수 없습니다.)")) return;
            Reservation.delete({reservation_id: reservation.reservation_id}, function ($response) {
                reload();
            })
        }

        function open_datepicker($event) {
            $event.preventDefault();
            $event.stopPropagation();
            $scope.datepicker.opened = true;
        }

        function search_reservation(dt) {
            /* reservation받아온 후 클라이언트 측에서 정렬 및 필터링 할 때 사용 */
            $scope.date_from = new Date(dt.getFullYear(), dt.getMonth(), dt.getDate());
            $scope.date_to = new Date(dt.getFullYear(), dt.getMonth(), dt.getDate() + 1, 0, 0, -1);
            $scope.reservations_filtered = $filter('date_filter')($scope.reservations, $scope.date_from, $scope.date_to)
        }

        function open_modal_external($event, content_time) {
            $event.preventDefault();
            $event.stopPropagation();
            var modalInstance = $modal.open({
                templateUrl: '/admin/modals/externalReservationModal.html',
                controller: 'externalReservationModalController',
                size: 'lg',
                resolve: {
                    content: function () {
                        return $scope.content;
                    },
                    content_time: function () {
                        return $scope.content_time;
                    }
                }
            }).result.then(function () {
                    reload()
                })
        }

        function change_capacity(content_time) {
            var modalInstance = $modal.open({
                templateUrl: '/admin/modals/changeCapacityModal.html',
                controller: 'changeCapacityModalController',
                size: 'xs',
                resolve: {
                    content_time: function () {
                        return content_time;
                    }
                }
            }).result.then(function () {
                    reload()
                })
        }

    }]).filter('date_filter', function () {
    return function (items, from, to) {
        if (!items) {
            return items;
        } // not loaded yet
        var result = [];
        for (var i = 0; i < items.length; i++) {
            var time = items[i].content_time.date;
            if (time instanceof String) {
                time = new Date(time)
            }

            if (!to || time > to) {
                continue;
            }
            if (!from || time < from) {
                continue;
            }
            result.push(items[i])
        }
        return result;
    }
});


app.controller('adminReservationController', ['$scope', '$rootScope', '$routeParams', '$filter', '$modal', '$location', '$window',
    'Company', 'Content', 'ContentTime', 'Reservation', 'SMS',
    function ($scope, $rootScope, $routeParams, $filter, $modal, $location, $window,
              Company, Content, ContentTime, Reservation, SMS) {
        $scope.approve = approve;
        $scope.reject = reject;
        $scope.set_watched = set_watched;
        $scope.delete = delete_reservation;
        $scope.open_datepicker = open_datepicker;
        $scope.filter_date= filter_date;
        $scope.go_back = go_back_history;
        $scope.search = search;

        $scope.datepicker = {}; // datepicker.opened용. primitive이면 에러남
        $scope.datepicker_format = 'yyyy년 MM월 dd일';
        $scope.dateoptions = {
            showWeeks:false
        };
        $scope.waiting = true;
        $scope.is_new = $routeParams['new']==='new';

        reload();

        function reload(){
            load_company();
            load_reservation();
        }

        if ($routeParams['date']) {
            $scope.dt = new Date($routeParams['date'])
        }

        function load_company() {
            Company.get_current(function(response){
                $rootScope.company = response;
            });
        }

        function load_reservation() {
            Reservation.simple_get({'new': $scope.is_new}, function(response){
                $scope.reservations = response.objects;
                for(var i= 0; i<$scope.reservations.length; i++){
                    $scope.reservations[i].content_time.date = Date.parse($scope.reservations[i].content_time.date)
                }
                $scope.reservations_filtered = $scope.reservations;
                $scope.waiting = false;
            });
        }


        function go_back_history() {
            $window.history.back();
        }


        function approve(reservation) { // can't get reservation directly as a parameter because we need to update $scope
            if (reservation.status != 1) {
                $scope.waiting = true;
                Reservation.update({reservation_id: reservation.reservation_id}, {status: 1}, function ($response) {
                   SMS.send({
                        phone_number: reservation.manager_phone,
                        content: '[ 에듀티켓-예약 완료 ]\n' +
                                 '입장안내입니다. 공연장 입구에서 본 문자내역을 보여주세요.\n' +
                                 '\n' +
                                 moment(reservation.content_time.date).format('M월 D일') + reservation.organization_name + ' ' + reservation.manager_name + '선생님 예약내역입니다.\n' +
                                 reservation.content.name + ' | ' + reservation.charged + '명 예약 | 인솔자 ' + reservation.chargeless + '명 무료\n' +
                                 '\n' +
                                 '관람 후 결제청구서가 발송됩니다.\n'
                   });
                    reload();
                });
            }
        }

        function reject(reservation) { // can't get reservation directly as a parameter because we need to update $scope
            if (reservation.status != 1) {
                $scope.waiting = true;
                Reservation.update({reservation_id: reservation.reservation_id}, {status: 6}, function ($response) {
                    reload();
                });
            }
        }

        function set_watched(reservation) {
            /* 관람 확인 시 실제로 본 인원 수 입력 */
            var modalInstance = $modal.open({
                templateUrl: '/admin/modals/watchedModal.html',
                controller: 'watchedModalController',
                size: 'lg',
                resolve: {
                    reservation: function () {
                        return reservation;
                    }
                }
            }).result.then(function () {
                    reload()
                })
        }

        function delete_reservation(reservation) {
            if(!confirm("정말로 삭제하시겠습니까?\n(이 작업은 되돌릴 수 없습니다.)")) return;
            Reservation.delete({reservation_id: reservation.reservation_id}, function ($response) {
                reload();
            })
        }

        function open_datepicker($event) {
            $event.preventDefault();
            $event.stopPropagation();
            $scope.datepicker.opened = true;
        }

        function filter_date(dt) {
            /* reservation받아온 후 클라이언트 측에서 정렬 및 필터링 할 때 사용 */
            $scope.date_from = new Date(dt.getFullYear(), dt.getMonth(), dt.getDate());
            $scope.date_to = new Date(dt.getFullYear(), dt.getMonth(), dt.getDate() + 1, 0, 0, -1);
            $scope.reservations_filtered = $filter('date_filter')($scope.reservations, $scope.date_from, $scope.date_to)
        }

        function search(){
            $scope.reservations_filtered = $scope.reservations;
            if($scope.dt){
                filter_date($scope.dt);
            }
            if($scope.name){
                // 공연명으로 필터링
                var temp_reservations = []
                for(var i=0; i< $scope.reservations_filtered.length; i++){
                    console.log($scope.reservations_filtered[i].content.name)
                    if($scope.reservations_filtered[i].content.name.indexOf($scope.name) > -1){ // 검색된 공연명이 포함되는 모든 공연 검색
                        temp_reservations.push($scope.reservations_filtered[i])
                    }
                }
                $scope.reservations_filtered = temp_reservations;
            }
        }



    }]).filter('date_filter', function () {
    return function (items, from, to) {
        if (!items) {
            return items;
        } // not loaded yet
        var result = [];
        for (var i = 0; i < items.length; i++) {
            var time = items[i].content_time.date;
            if (time instanceof String) {
                time = new Date(time)
            }

            if (!to || time > to) {
                continue;
            }
            if (!from || time < from) {
                continue;
            }
            result.push(items[i])
        }
        return result;
    }
});

app.controller('resolvedModalController', function ($scope, $modalInstance) {
    $scope.cancel = function () {
        $modalInstance.dismiss('cancel');
    }
});
app.controller('modalInstanceController', function ($scope, $modalInstance) {
    $scope.ok = function () {
        $modalInstance.close($scope.watched_count);
    };
    $scope.cancel = function () {
        $modalInstance.dismiss('cancel');
    }
});
app.controller('externalReservationModalController', ['$scope', '$modalInstance', 'Reservation', 'content_time',
    function ($scope, $modalInstance, Reservation, content_time) {
        $scope.cancel = function () {
            $modalInstance.dismiss('cancel');
        };
        $scope.create_reservation = function (reservation) {
            if (reservation.vendor==='에듀티켓'){
                alert('타영업사명은 에듀티켓일 수 없습니다.');
                return;
            }
            if (parseInt(reservation.charged) + parseInt(reservation.chargeless) > content_time.remaining_seat) {
                alert('인원이 총 좌석 수를 초과하였습니다. 인원을 확인하고 다시 시도해주세요. (잔여좌석 수 : ' + content_time.remaining_seat + ')');
                return;
            }
            reservation.content_time_id = content_time.content_time_id;
            reservation.status = 2;
            reservation.payment_method = 0;
            reservation.password = '0000';
            $scope.waiting = true;
            Reservation.create(reservation, function () {
                $scope.waiting = false;
                $modalInstance.close('ok');
            });
        }
    }]);

app.controller('watchedModalController', ['$scope', '$modalInstance', 'Reservation', 'reservation',
    function ($scope, $modalInstance, Reservation, reservation) {
        $scope.cancel = function () {
            $modalInstance.dismiss('cancel');
        };
        $scope.set_watched_reservation = function (watched_count) {
            Reservation.update({reservation_id: reservation.reservation_id},
                {
                    reservation_id: reservation.reservation_id,
                    status: 3,
                    watched_count: watched_count
                },
                function (response) {
                    $modalInstance.close('ok');
                });
        }
    }]);

app.controller('changeCapacityModalController', ['$scope', '$modalInstance', 'ContentTime', 'content_time',
    function ($scope, $modalInstance, ContentTime, content_time) {
        $scope.capacity = content_time.assigned_capacity;
        $scope.content_time = content_time;
        $scope.cancel = function () {
            $modalInstance.dismiss('cancel');
        };
        $scope.set_capacity = function (capacity) {
            ContentTime.update({content_time_id: content_time.content_time_id},
                {
                    assigned_capacity: capacity
                },
                function (response) {
                    $modalInstance.close('ok');
                });
        }
    }]);
