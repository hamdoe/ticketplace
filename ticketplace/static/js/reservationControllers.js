'use strict';

app = angular.module('reservationApp');
app.factory('reservation_preserver', function () {
    //returns an empty object that is persistent in app
    return {};
});
app.controller('reservationSearchController', ['$scope',
    function ($scope) {
        $scope.search = function(phone){
            if (/^\d{3}\d{3,4}\d{4}$/.test($scope.phone)) {
                $scope.phone = $scope.phone.replace(/^(\d{3})(\d{3,4})(\d{4})$/, '$1-$2-$3')
            }
            location.href = "reservation#/result?phone="+phone;
        };
    }]);
app.controller('reservationNewController', ['$scope', '$routeParams', '$location', '$window', '$modal', 'Reservation', 'ContentTime', 'reservation_preserver',
    function ($scope, $routeParams, $location, $window, $modal, Reservation, ContentTime, reservation_preserver) {
        $scope.go_back_history = go_back_history;
        $scope.open_modal = open_modal;
        $scope.authenticated = false;
        $scope.send = send;

        $scope.reservation = reservation_preserver; // note that this preserves data when user comes back
        if (!Object.keys($scope.reservation).length) { // if loaded reservation object is empty
            var content_time_id = $routeParams['content_time'];
            //if (!content_time_id) {
            //    alert('잘못된 접근입니다.');
            //    $location.path('/index');
            //    $location.replace();
            //    return;
            //}

            ContentTime.get({content_time_id: content_time_id}, function ($response) {
                $scope.content_time = $response;
                if ($routeParams['total_headcount'] && (!$scope.reservation.total_headcount)) {
                    $scope.reservation.total_headcount = $routeParams['total_headcount'];
                    $scope.chargeless_limit = Math.ceil($scope.reservation.total_headcount / 20);
                }
                if ($routeParams['organization_type'] && (!$scope.reservation.organization_type)) {
                    $scope.reservation.organization_type = $routeParams['organization_type'];
                }
                if ($routeParams['payment_method'] && (!$scope.reservation.payment_method)) {
                    $scope.reservation.payment_method = $routeParams['payment_method'];
                }

                $scope.reservation.content_time_id = content_time_id;
                $scope.reservation.content_time = $scope.content_time;
                $scope.submit = function () {
                    reservation_preserver = $scope.reservation;
                    $location.path('/confirm')
                }
            });
        }
        else {
            $scope.content_time = $scope.reservation.content_time;
            $scope.authenticated = true;
            $scope.submit = function () {
                reservation_preserver = $scope.reservation;
                $location.path('/confirm')
            }
        }

        function go_back_history() {
            $window.history.back();
        }

        function open_modal(form) {
            console.dir(form)
            if (!$scope.reservation.manager_name) {
                alert('담당자 이름을 입력해주세요.');
                return;
            }
            if (/^\d{3}\d{3,4}\d{4}$/.test($scope.reservation.manager_phone)) {
                $scope.reservation.manager_phone = $scope.reservation.manager_phone.replace(/^(\d{3})(\d{3,4})(\d{4})$/, '$1-$2-$3')
            }
            if (!$scope.reservation.manager_phone || !/^\d{3}-\d{3,4}-\d{4}$/.test($scope.reservation.manager_phone)) {

                // 주의: angular기 form validation을 할 때 안맞으면 아예 변수 설정이 안됨
                // 즉, 그냥 변수가 undefined인지만 확인해도 이론상 되기는 함.
                alert('연락처 입력 형식이 올바르지 않습니다.\n하이픈(-)을 포함하여 010-1234-5678 형태로 입력해주세요.')
                return;
            }

            var modalInstance = $modal.open({
                templateUrl: 'identificationModal.html',
                controller: 'identificationModalInstanceController',
                resolve: {
                    reservation: function () {
                        return $scope.reservation;
                    }
                }
            });

            modalInstance.result.then(function () {
                $scope.authenticated = true;
            })
        }

        function send(){
            if($scope.form.$invalid){
                focus_first_invalid($scope.form);
                return;
            }
            if(!$scope.authenticated){
                form['manager_phone'].focus();
                return;
            }
            if(!$scope.agreed1){
                form['optionsCheckbox1'].focus();
                return;
            }
            if(!$scope.agreed2){
                form['optionsCheckbox2'].focus();
                return;
            }
            $location.path('/confirm');
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
    }]).config(['$tooltipProvider', function($tooltipProvider){
        $tooltipProvider.setTriggers({
            'show': 'hide'
        });
    }]);


app.controller('identificationModalInstanceController', ['$scope', '$modalInstance', '$window', 'OTP', 'reservation',
    function ($scope, $modalInstance, $window, OTP, reservation) {
        $scope.reservation = reservation;
        $scope.timeover = timeover;
        $scope.is_timer_running = false;
        $scope.waiting = false;
        $scope.send_otp = send_otp;
        $scope.check_otp = check_otp;
        $scope.cancel = cancel;
        $scope.reservation.vendor = "에듀티켓";
        function cancel() {
            $modalInstance.dismiss('cancel');
        }

        function send_otp() {
            $scope.waiting = true;
            OTP.create({name: reservation.manager_name, phone_number: reservation.manager_phone}, function (response) {
                console.log(response);
                if (response.hasOwnProperty('error')) {
                    alert('OTP생성중 에러가 발생하였습니다. 이름과 전화번호를 확인하시고 다시 시도해주세요.')
                    $scope.waiting = false;
                    return;
                }
                $scope.waiting = false;
                start_timer();
            })
        }

        function check_otp(otp) {
            $scope.waiting = true;
            console.log('validating otp : ', otp);
            OTP.get({otp: otp}, function (response) {
                console.log(response);
                if (response.hasOwnProperty('error')) {
                    alert(response.error);
                    $scope.waiting = false;
                    return;
                }
                $scope.waiting = false;
                $modalInstance.close();
            })
        }

        function timeover() {
            $scope.is_timer_running = false;
            $scope.$apply();
            console.log('time over!')
        }

        function start_timer() {
            $scope.$broadcast('timer-start');
            $scope.is_timer_running = true;
        }

        send_otp();

    }]);


app.controller('reservationSearchController', ['$window', function($window){
    // 레거시 지원용
    $window.location.href='/reservation/search'
}]);

app.controller('reservationConfirmController', ['$scope', '$http', 'Email', 'SMS', 'Reservation', '$route', '$location', 'reservation_preserver',
    function ($scope, $http, Email, SMS, Reservation, $route, $location, reservation_preserver) {
        $scope.reservation = reservation_preserver;
        $scope.go_back = go_back;
        $scope.done = false;
        $scope.submit = submit;

        //if (!('content_time_id' in $scope.reservation)) {
        //    alert('잘못된 접근입니다.');
        //    location.href = "/index";
        //    return;
        //}

        function go_back() {
            $location.path('/new').search(
                {
                    content_time: $scope.reservation.content_time_id,
                    organization_type: $scope.reservation.organization_type,
                    charged: $scope.reservation.charged
                }
            )
        }

        function submit() {
            $scope.waiting = true;
            Reservation.create($scope.reservation, function () {
                alert('성공적으로 예약신청되었습니다. 문자로 확인메세지가 발송됩니다.');
                $scope.done = true;

                // 문자 임시로 브라우저에서 보냄
                var date = moment($scope.reservation.content_time.date);

                SMS.send({
                    phone_number: $scope.reservation.manager_phone,
                    content: '[ 에듀티켓-예약신청 접수완료 ] ' + $scope.reservation.manager_name + '선생님께서 '+
                    date.format('M월 D일 H시 m분') +'에 진행되는 연극' + $scope.reservation.content_time.content.name + ' 단체예약을 신청하셨습니다. 승인안내는 하루 내에 sms로 전송됩니다.\n'
                    + '공연 예약내역은 에듀티켓 사이트 상단의 예약조회페이지에서 확인하실 수 있습니다. http://eduticket.kr/reservation/search'
                }, function(success){
                    // 문자 잘 보내졌나 확인한 뒤에 redirect
                    $location.path('/search');
                    $location.replace();
                });
                SMS.send({
                    phone_number: '010-4014-2193',
                    content: date.format('YY년 M월 D일 H시 m분') + ' ' + $scope.reservation.organization_name + '단체가 연극 ' + $scope.reservation.content_time.content.name + ' 단체예약을 신청하셨습니다.'
                });
                return;
            }, function(error){
                alert('오류가 발생하였습니다.');
                console.log(error);
            });
        }

    }]);


app.controller('reservationResultController', ['$scope', 'Reservation', 'Content', '$routeParams', '$location', '$modal',
    function ($scope, Reservation, Content, $routeParams, $location, $modal) {
        $scope.phone = $routeParams['phone'];
        if (/^\d{3}-?\d{3,4}-?\d{4}$/.test($scope.phone)) {
            $scope.phone = $scope.phone.replace(/^(\d{3})(\d{3,4})(\d{4})$/, '$1-$2-$3')
        }
        console.log($scope.phone)

        Reservation.get({q: {filters: [{val: $scope.phone, op: '==', name: 'manager_phone'}]}}, function ($response) {
            $scope.reservations = $response.objects;
            for (var i in $scope.reservations) {
                var reservation = $scope.reservations[i];
                $scope.reservations[i].content_time.content = Content.get({content_id: reservation.content_time.content_id});
            }
        });
        $scope.open_modal = open_modal;
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
    }]);

app.controller('modalInstanceController', ['$scope', '$modalInstance', '$window', 'Reservation', 'reservation',
    function ($scope, $modalInstance, $window, Reservation, reservation) {

        $scope.reservation = reservation;
        $scope.printModal = printModal;
        $scope.cancel_reservation = cancel_reservation;

        function printModal() {
            var printContents = document.getElementsByClassName('modal-dialog')[0].innerHTML;
            var popupWin = window.open('', '_blank', 'width=300,height=300');
            popupWin.document.open()
            popupWin.document.write('<html><head><link href="/static/css/bootstrap.min.css" rel="stylesheet">' +
                '<link href="/static/css/tp.css" rel="stylesheet">' +
                '<link href="/static/css/menu-color.css" rel="stylesheet">' +
                '<link href="/static/css/panel-tab.css" rel="stylesheet">' +
                '<link href="/static/css/font-awesome.min.css" rel="stylesheet">' +
                '<link href="/static/css/common.css" rel="stylesheet">' +
                '</head><body onload="window.print()">' + printContents + '</html>');
            popupWin.document.close();
        }

        function cancel_reservation() {
            if (reservation.status == 5) {
                alert('이미 취소된 예약입니다.');
                return;
            }
            var password = prompt("비밀번호를 입력해주세요.");
            if (password) {
                if (password == reservation.password) {
                    Reservation.update({
                        reservation_id: reservation.reservation_id,
                        status: 5,
                        password: password
                    }, function (response) {
                        alert('예약이 성공적으로 취소되었습니다.');
                        $scope.cancel();
                        $window.location.reload();
                    })
                }
                else {
                    alert('비밀번호를 확인하시고 다시 입력해주세요.')
                }
            }
        }

        $scope.ok = function () {
            $modalInstance.close($scope.watched_count);
        };
        $scope.cancel = function () {
            $modalInstance.dismiss('cancel');
        };
    }]);

