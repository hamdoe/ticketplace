var app = angular.module('reservationApp', ['ngResource', 'ngRoute',
    'ui.bootstrap', 'timer',
    'reservationServices', 'contentTimeServices', 'contentServices', 'utilityServices',
    'reservationFilters'
])
.config(function($interpolateProvider){
    $interpolateProvider.startSymbol('{[{').endSymbol('}]}');
})
    .config(['$routeProvider',
        function ($routeProvider) {
            $routeProvider.
                when('/confirm', {
                    templateUrl: 'customer/partials/reservation_confirm.html',
                    controller: 'reservationConfirmController'
                }).
                when('/new', {
                    templateUrl: 'customer/partials/reservation_new.html',
                    controller: 'reservationNewController'
                }).
                when('/result', {
                    templateUrl: 'customer/partials/reservation_result.html',
                    controller: 'reservationResultController'
                }).
                when('/search', {
                    template: "<div></div>",
                    controller: 'reservationSearchController'
                }).
                otherwise(
                {
                    /*

                        잘못된 접근일 때 인덱스로 이동하도록 한다.

                     */
                    controller: function () {
                        window.location.replace('/');
                    }
                });
        }]);


angular.module('reservationFilters', []).filter('reservation_status_filter', ['$sce',
    function ($sce) {
        return function (status) {
            return {
                0: $sce.trustAsHtml('<span class="r-wait">승인대기</span>'),
                1: $sce.trustAsHtml('<span class="r-approv">승인</span>'),
                2: $sce.trustAsHtml('<span class="r-approv">승인</span>'),
                3: $sce.trustAsHtml('<span class="r-approv">승인</span>'),
                4: $sce.trustAsHtml('<span class="r-wait">승인대기</span>'),
                5: $sce.trustAsHtml('<span class="r-cancel">취소</span>'),
                6: $sce.trustAsHtml('<span class="r-cancel">예약거절</span>')
            }[status]
        }
    }])
    .filter('reservation_payment_filter', ['$sce',
        function ($sce) {
            return function (status) {
                return {
                    0: $sce.trustAsHtml('<span class="waiting">결제 대기</span>'),
                    1: $sce.trustAsHtml('<span class="complete">결제 완료</span>'),
                    2: $sce.trustAsHtml('<span class="complete">결제 완료</span>')
                }[status]
            }
        }])
    .filter('organization_type_filter', [
        function () {
            return function (organization_type) {
                return {
                    0: "일반",
                    1: "유치원",
                    2: "초등학교",
                    3: "중학교",
                    4: "고등학교"
                }[organization_type]
            }
        }])
    .filter('payment_method_filter', [
        function () {
            return function (payment_method) {
                return {
                    0: "계좌 이체(후불)",
                    1: "현장 결제"
                }[payment_method]
            }
        }])


// from http://jsfiddle.net/webvitaly/AG2wf/1/light/
function isEmpty(value) {
    return angular.isUndefined(value) || value === '' || value === null || value !== value;
}
app.directive('ngMax', function () {
    return {
        restrict: 'A',
        require: 'ngModel',
        link: function (scope, elem, attr, ctrl) {
            scope.$watch(attr.ngMax, function () {
                ctrl.$setViewValue(ctrl.$viewValue);
            });
            var maxValidator = function (value) {
                if(typeof(attr.ngMax) === "number"){
                    var max = attr.ngMax;
                }
                else{
                    var max = scope.$eval(attr.ngMax) || Infinity;
                }
                if (!isEmpty(value) && value > max) {
                    ctrl.$setValidity('ngMax', false);
                    return undefined;
                } else {
                    ctrl.$setValidity('ngMax', true);
                    return value;
                }
            };

            ctrl.$parsers.push(maxValidator);
            ctrl.$formatters.push(maxValidator);
        }
    };
});
