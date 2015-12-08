var app = angular.module('contentApp', ['ngResource', 'ngSanitize', 'ngRoute',
    'ui.bootstrap', 'ui.bootstrap.tpls',
    'contentServices', 'contentFilters'])
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

angular.module('contentFilters', [])
    .filter('genre', function(){
        return function(genre){
            return {
                0: '공연',
                1: '전시'
            }[genre];
        }
    })
    .filter('actor_change', function(){
        return function(genre){
            return {
                0: '변경 없음',
                1: '변경 있음'
            }[genre];
        }
    })
    .filter('location', function(){
        return function(genre){
            return {
                0: '대학로',
                1: '서울',
                2: '경기',
                3: '인천',
                4: '기타'
            }[genre];
        }
    })