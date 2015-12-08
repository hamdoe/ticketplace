var app = angular.module('indexApp', ['ngResource',
    'contentServices', 'companyServices', 'utilityServices', 'signatureServices'])
.config(function($interpolateProvider){
    $interpolateProvider.startSymbol('{[{').endSymbol('}]}');
})
