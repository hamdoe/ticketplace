var app = angular.module('sadminApp', [
    'ngResource', 'ngRoute', 'angularFileUpload', 'ui.bootstrap', 'ui.bootstrap.tpls',
    'contentServices', 'companyServices', 'contentTimeServices', 'reservationServices',
    'signatureServices'
])
.config(function($interpolateProvider){
    $interpolateProvider.startSymbol('{[{').endSymbol('}]}');
})
.config(['$routeProvider',
    function($routeProvider){
        $routeProvider.
            when('/',{
                templateUrl: 'sadmin/partials/index.html'
            }).
            when('/index',{
                templateUrl: 'sadmin/partials/index.html'
            }).
            when('/member',{
                templateUrl: 'sadmin/partials/member.html'
            }).
            when('/content',{
                templateUrl: 'sadmin/partials/contents.html',
                controller: 'sadminContentController'
            }).
            when('/time',{
                templateUrl: 'sadmin/partials/time_manage.html'
            }).
            when('/notice',{
                templateUrl: 'sadmin/partials/notice.html'
            }).
            when('/notice/modify',{
                templateUrl: 'sadmin/partials/notice_modify.html'
            }).
            when('/notice/view',{
                templateUrl: 'sadmin/partials/notice_view.html'
            }).
            when('/notice/write',{
                templateUrl: 'sadmin/partials/notice_write.html'
            }).
            when('/qna',{
                templateUrl: 'sadmin/partials/qna.html'
            }).
            when('/qna/view',{
                templateUrl: 'sadmin/partials/qna_view.html'
            }).
            when('/qna/write',{
                templateUrl: 'sadmin/partials/qna_write.html'
            }).
            when('/reservation',{
                templateUrl: 'sadmin/partials/reserve_manage.html',
                controller: 'sadminReservationController'
            }).
            when('/etc',{
                templateUrl: 'sadmin/partials/etc_manage.html'
            }).
            when('/statistics',{
                templateUrl: 'sadmin/partials/stat.html'
            })
    }]);