'use strict';

/*

    use forEach for ie8
    Array에 forEach를 추가하기 위한 코드.
    김민준이 Ctrl+C,V해서 본인도 자세히는 이해하지 못하고 있을 듯 함.
        -> 이해하고 있다고 반박당함 (김민준 : "이해할게 뭐 있냐")

 */
if (typeof Array.prototype.forEach != 'function') {
    Array.prototype.forEach = function(callback){
      for (var i = 0; i < this.length; i++){
        callback.apply(this, [this[i], i, this]);
      }
    };
}

/*

    변수로 넘겨진 suffix로 끝나는지 확인하는 함수.

 */
String.prototype.endsWith = function(suffix) {
    return this.indexOf(suffix, this.length - suffix.length) !== -1;
};

/*

    parseGetManyDates : response의 data가 List일 때.
    parseGetResponseDates : response의 data가 하나의 Object일 때.
    김민준 : "하나로 묶어야 하지 않나?"
    한세진 : "나중에 해, 나중에"

    date로 끝나는 (ex. created_date, modified_date) 데이터(속성)들을
    Date 객채로 parsing 해준다.
    hasOwnProperty를 체크하는 목적은, 상위 프로토타입 체인에 없는 속성들만
    작업을 해 주기 위해서이다.

 */
function parseGetManyDates(response){
    response.data.objects.forEach(function(object){
        for(var key in object) {
            if(!object.hasOwnProperty(key)){
                continue;
            }
            if(key.endsWith('date')){
                // timezone문제의 땜빵입니다. 죄송합니다.
                object[key] = Date.parse(object[key]);
            }
        }
    });
    return response;
}

function parseResponseDates(response) {
    // string to date for every '~_date'
    var data = response.data;
    for(var key in data) {
        if(!data.hasOwnProperty(key)){
            continue;
        }
        if(key.endsWith('date')){
            data[key] = Date.parse(data[key]);
        }
    }
    return response;
}

/*

    아래의 코드들은 AngularJS 모듈을 만들기 위한 것이다.
    주석을 작성하는 @sejin은 AngularJS를 학습한지 오래되어 모듈 작성법이 기억이 나지 않아 공부를 해 보았다.

    Write custom module for AngularJS: http://stackoverflow.com/questions/19109291/write-custom-module-for-angularjs
    위 주소를 참조하라.


    $resource의 사용법 (by 김민준, 한세진이 정리)

    대충 설명하자면
    Email = $resource('/api/email',{}, {send:{method:'GET'}}) 로 저장해서
    Email.send({'text':'hi'})로 보내면
    /api/email?text=hi가 된다.

 */
var utilityServices  = angular.module('utilityServices', ['ngResource']);
utilityServices.factory('Email', ['$resource',
    function($resource){
        return $resource('/api/email',{}, {send:{method:'POST'}})
    }
]);

utilityServices.factory('SMS', ['$resource',
    function($resource){
        return $resource('/api/sms',{}, {send:{method:'POST'}})
    }
]);

utilityServices.factory('OTP', ['$resource',
    function($resource){
        return $resource('/api/otp/:otp',{}, {
            create: {method:'POST'},
            validate: {method: 'GET', params: {otp: '@otp'}}
        })
    }
]);

/*

    content, reservation, content time, company
    Q&A, Notice

    에 대한 CRUD를 제공한다.

 */
var companyServices = angular.module('companyServices', ['ngResource']);

companyServices.factory('Company',['$resource',
    function($resource){
        return $resource('api/company/:company_id',{}, {
            get_current: { method:'GET', url: 'api/admin/company'},
            query: { method:'GET'},
            create: { method: 'POST'},
            get : { method:'GET', params: {company_id :'@company_id'} },
            update: { method: 'PUT', params: {company_id: '@company_id'} },
            delete: { method: 'DELETE', params: {company_id: '@company_id'} }
        });
    }]);

var contentServices = angular.module('contentServices', ['ngResource']);

contentServices.factory('Content', ['$resource',
    function($resource){
        return $resource('api/content/:content_id', {}, {
            query: { method:'GET', interceptor:{response:parseGetManyDates} },
            create: { method: 'POST'},
            get : { method:'GET', params: { content_id:'@content_id'}, interceptor:{response:parseResponseDates} },
            update: { method: 'PUT', params: {content_id: '@content_id'} },
            delete: { method: 'DELETE', params: {content_id: '@content_id'} }
        });
    }]);

var contentTimeServices = angular.module('contentTimeServices',['ngResource']);

contentTimeServices.factory('ContentTime', ['$resource',
    function($resource){
        return $resource('api/content_time/:content_time_id', {}, {
            query: { method:'GET'},
            create: { method: 'POST'},
            get : { method:'GET', params: { content_time_id:'@content_time_id'} },
            update: { method: 'PUT', params: {content_time_id: '@content_time_id'} },
            delete: { method: 'DELETE', params: {content_time_id: '@content_time_id'} }
        });
    }]);

var reservationServices = angular.module('reservationServices', ['ngResource']);

reservationServices.factory('Reservation', ['$resource',
    function($resource){
        return $resource('api/reservation/:reservation_id', {}, {
            simple_get : { method:'GET', url:'api/admin/reservation'},
            query: { method:'GET'},
            create: { method: 'POST'},
            get : { method:'GET', params: { reservation_id:'@reservation_id'} },
            update: { method: 'PUT', params: { reservation_id: '@reservation_id'} },
            delete: { method: 'DELETE', params: { reservation_id: '@reservation_id'} }
        });
    }]);


var customerServices = angular.module('customerServices', ['ngResource']);

customerServices.factory('Notice',['$resource',
    function($resource){
        return $resource('api/notice/:notice_id',{}, {
            query: { method:'GET'},
            create: { method: 'POST'},
            get : { method:'GET', params: {notice_id :'@notice_id'} },
            update: { method: 'PUT', params: {notice_id: '@notice_id'} },
            delete: { method: 'DELETE', params: {notice_id: '@notice_id'} }
        });
    }]);

customerServices.factory('Qna',['$resource',
    function($resource){
        return $resource('api/qna/:notice_id',{}, {
            query: { method:'GET'},
            create: { method: 'POST'},
            get : { method:'GET', params: {qna_id :'@qna_id'} },
            update: { method: 'PUT', params: {qna_id: '@qna_id'} },
            delete: { method: 'DELETE', params: {qna_id: '@qna_id'} }
        });
    }]);

/*

    signature는 Amazon Cloud Server에 업로드를 하기 위함이다.

 */
var signatureServices = angular.module('signatureServices', ['ngResource']);

signatureServices.factory('Signature', ['$resource', function($resource){
        return $resource('/api/get_signature', null, {
            'get': {method:'GET'}
        });
    }]);
