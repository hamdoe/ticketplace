var app = angular.module('defaultApp', ['ngResource', 'customerServices', 'ngRoute'])
.config(function($interpolateProvider){
    $interpolateProvider.startSymbol('{[{').endSymbol('}]}');
})
.config(['$routeProvider',
    function($routeProvider){
        $routeProvider.
            when('/',{
                templateUrl: 'customer/partials/notice_list.html',
                controller: 'noticeListController' //TODO:복붙수정
            }).
            when('/notice',{
                templateUrl: 'customer/partials/notice_list.html',
                controller: 'noticeListController'
            }).
            when('/notice/:notice_id',{
                templateUrl: 'customer/partials/notice_view.html',
                controller: 'noticeViewController'
            }).
            when('/qna/',{
                templateUrl: 'customer/partials/qna_temp.html'
            }).
            when('/qna/:qna_id',{
                templateUrl: 'customer/partials/qna_view.html'
            }).
            when('/qna/write',{
                templateUrl: 'customer/partials/qna_write.html'
            }).
            when('/faq',{
                templateUrl: 'customer/partials/faq.html'
            })
    }]);
