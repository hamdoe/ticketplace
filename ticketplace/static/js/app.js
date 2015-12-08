var app = angular.module('defaultApp', ['ngResource',
    'angularFileUpload', 'ui.bootstrap', 'ui.bootstrap.tpls',
    'contentServices', 'companyServices', 'utilityServices', 'signatureServices'])
.config(function($interpolateProvider){
    $interpolateProvider.startSymbol('{[{').endSymbol('}]}');
})



//useful functions. Might need to separate these in to another file

String.prototype.capitalize = function() { //Capitalize first letter. Can be called by any string objects
    return this.charAt(0).toUpperCase() + this.slice(1);
};
String.prototype.pluralize = function() { //Dirty way to pluralize. will fix when shit hits the fan
    return this + 's';
};