'use strict';

/*

    제작사 페이지들의 집합이 하나의 AngularJS Application이 된다.
    사용하는 모듈 [시간날때 설명 추가]

    ngResource

    ngRoute
        현재 Best Practice가 아님.

    angularFileUpload

 */
var app = angular.module('adminApp', [
    'ngResource', 'ngRoute', 'angularFileUpload', 'ui.bootstrap', 'ui.bootstrap.tpls',
    'contentServices', 'companyServices', 'contentTimeServices', 'reservationServices', 'signatureServices', 'utilityServices',
    'productFilters'
])
.config(function($interpolateProvider){
    $interpolateProvider.startSymbol('{[{').endSymbol('}]}');
})
.config(['$routeProvider',
    function($routeProvider){
        /*

            Controller 등의 Javascript 파일은 처음 HTTP 요청이 있을때 모두 일괄적으로 가져온다.
            templateUrl에서 HTML 파일을 비동기적으로 가져온다.

         */
        $routeProvider.
            when('/',{
                templateUrl: 'admin/partials/index.html'
            }).
            when('/index',{
                templateUrl: 'admin/partials/index.html'
            }).
            when('/modify',{
                templateUrl: 'admin/partials/modify.html',
                controller: 'modifyCompanyController'
            }).
            when('/product/detail/:content_id',{
                templateUrl: 'admin/partials/time_content.html',
                controller: 'productDetailController'
            }).
            when('/product/:status',{
                templateUrl: 'admin/partials/product.html',
                controller: 'productController'
            }).
            when('/register',{
                templateUrl: 'admin/partials/register.html',
                controller: 'registerContentController'
            }).
            when('/reservation/content_time/:content_time_id',{
                templateUrl: 'admin/partials/time_reserv.html',
                controller: 'adminReservationPerContentTimeController'
            }).
            when('/reservation/:new',{
                templateUrl: 'admin/partials/reservation.html',
                controller: 'adminReservationController'
            })
    }]);
app.run(['$rootScope', function($rootScope){
        /*

            Flask로 처리해서 Javascript로 박아둠.
            수정이 필요함.
            (김민준 : Performance가 뛰어나다는 변명을 했음.)

         */
        $rootScope.current_user = current_user
    }
]);

angular.module('productFilters', []).filter('content_status_filter',[ '$sce',
function($sce){
    return function(status){
        return {
            0: $sce.trustAsHtml('<a href="#" type="button" class="btn btn-success btn-xs" disabled>작성 중</a>'),
            1: $sce.trustAsHtml('<a href="#" type="button" class="btn btn-warning btn-xs" disabled>판매 준비중</a>'),
            2: $sce.trustAsHtml('<a href="#" type="button" class="btn btn-danger btn-xs" disabled>등록 완료</a> '),
            3: $sce.trustAsHtml('<a href="#" type="button" class="btn btn-danger btn-xs" disabled>판매 종료</a>')
        }[status]
    }
}]).filter('payment_status_filter',[
function(){
    return function(status){
        return {
            0: '미결제',
            1: '결제 완료',
            2: '정산 완료'
        }[status]
    }
}]).filter('content_status_filter',[
function(){
    return function(status){
        return {
            0: '작성중',
            1: '등록신청중',
            2: '판매중',
            3: '판매완료'
        }[status]
    }
}]).filter('content_time_status_filter',[
function(){
    return function(status){
        return {
            0: '판매중',
            1: '마감'
        }[status]
    }
}]).filter('reservation_page_filter',
function(){
    return function(is_new){
        return {
            'new': '신규예약',
            'all': '전체예약 현황'
        }[is_new]
    }
}).filter('reservation_status_filter', [
function(){
    return function(status){
        return {
            0: '승인대기',
            1: '승인',
            2: '승인',
            3: '관람완료',
            4: '승인대기',
            5: '취소',
            6: '거절'
        }[status]
    }
}]);