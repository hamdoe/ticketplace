'use strict';

function getQueryVariable(variable) {
    // url의 get parameter를 파싱하는 함수
    var query = window.location.search.substring(1);
    var vars = query.split('&');
    for (var i = 0; i < vars.length; i++) {
        var pair = vars[i].split('=');
        if (decodeURIComponent(pair[0]) == variable) {
            return decodeURIComponent(pair[1]);
        }
    }
    console.log('Query variable %s not found', variable);
}

function getAllQueryVariable() {
    // url의 get parameter를 파싱해서 모두 가져오는 함수
    var query = window.location.search.substring(1);
    var vars = query.split('&');
    var params = {}
    for (var i = 0; i < vars.length; i++) {
        var pair = vars[i].split('=');
        params[decodeURIComponent(pair[0])] = decodeURIComponent(pair[1]);
    }
    return params;
}
function serialize(obj) {
    // params 을 get query string으로 바꾸는 serializing function
    var str = [];
    for(var p in obj)
        if (obj.hasOwnProperty(p)) {
            str.push(encodeURIComponent(p) + "=" + encodeURIComponent(obj[p]));
        }
    return str.join("&");
}

app = angular.module('contentApp');
app.controller('detailController', ['$scope', '$sce', '$location', 'Content',
    function ($scope, $sce, $location,  Content) {
        $scope.related_contents = [];
        $scope.load_daum_map = load_daum_map;
        // loading을 탭을 클릭할 때 함

        var content_id = getQueryVariable('content_id');
        Content.get({content_id: content_id}, function ($response) {
            $scope.content = $response.data;

            $(document).ready(function(){ // visiable안하면 맵이 로딩이 안되므로 잠시 tab2를 active시킴
                $(function() {
                    $('#home').removeClass('active');
                    $('#tab2').addClass('active');
                    load_daum_map($scope.content.latitude, $scope.content.longitude);
                    //$('.wrap_map').remove();
                    //$('.wrap_controllers').remove();  //교통편 기능 용. 기능 보류됨
                    $('#home').addClass('active');
                    $('#tab2').removeClass('active');
                });
            });

        });
        function load_daum_map(latitude, longtitude){
            var container = document.getElementById('map2');
            var options = {
                center: new daum.maps.LatLng(latitude, longtitude),
                level: 3
            };

            var map = new daum.maps.Map(container, options);
            var markerPosition  = new daum.maps.LatLng(latitude, longtitude); // 마커가 표시될 위치
            var marker = new daum.maps.Marker({ // 마커를 생성
                position: markerPosition
            });
            marker.setMap(map); // 마커가 지도 위에 표시되도록 설정합니다

        }
    }]);

app.controller('listController', ['$scope', '$routeParams', '$route', '$location', '$window', 'dateFilter','Content',
    function ($scope, $routeParams, $route, $location, $window, dateFilter, Content) {

        $scope.open_datepicker = open_datepicker;
        $scope.datepicker_format = 'yyyy년 MM월 dd일';
        $scope.search = search;
        $scope.waiting = true;
        $scope.location_selected = {}; // 지역검색 시 selectmenu의 선택된 상태를 저장

        var params = getAllQueryVariable();
        if('location' in params){
            $scope.location = params['location'];
            $scope.location_selected[$scope.location] = true; // 지역 selectmenu에서 선택된 상태로
        }
        if('date' in params){
            $scope.date = params['date'];
        }
        if('headcount' in params){
            $scope.headcount = params['headcount'];
        }

        load_contents();



        function search(){
            if($scope.location){
                params['location'] = $scope.location;
            }
            if($scope.date){
                params['date'] = dateFilter($scope.date, 'yyyy-MM-dd')
            }
            if($scope.headcount){
                params['headcount'] = $scope.headcount;
            }
            $window.location.href = 'content/list?' + serialize(params);
        }
        function open_datepicker($event){
            $event.preventDefault();
            $event.stopPropagation();
            $scope.opened_datepicker = true;
        }


        function load_contents() {
            $scope.waiting = true;
            var q = generate_q(params);
            Content.query(q, function ($response) {
                $scope.contents = $response.data.objects;
                $scope.waiting = false;
            });
        }

        function generate_q(params){
            // generates query via given parameters
            var filter = function(name, op, val){return {name:name, op:op, val:val}};

            var query = {filters: []};
            query.filters.push(filter('status','==', 2)) // 공연 판매 중인 것만 표시
            var q = {q: query};
            q.results_per_page = 30;

            for(var param in params){
                if(!params.hasOwnProperty(param))
                    { continue; }

                switch(param){
                    case 'content_type':
                        var content_type = params.content_type;
                        var content_type_filters = [[filter('age_min', '<', 8)],
                        [filter('age_max', '>', 7), filter('age_min', '<', 13)],
                        [filter('age_max', '>', 12)]];
                        query.filters = query.filters.concat(content_type_filters[content_type]); // concats multiple objects
                        break;
                    case 'genre':
                        query.filters.push(filter('genre', '==', params.genre));
                        break;
                    case 'location':
                        query.filters.push(filter('location', '==', params.location));
                        break;
                    case 'search':
                        query.filters.push(filter('name', 'like', '%' + params.search + '%'));
                        break;
                    case 'headcount': // date과의 and조건때문에 파이썬에서 처리해 주기로 함
                        query.headcount = params.headcount;
                    //    query.filters.push(filter('content_time_list', 'any', filter('remaining_seat', '>=', params.headcount)));
                        break;
                    case 'date':
                        query.date = params.date;
                        break;
                    default: // notably page and result_per_page
                        q[param] = params[param];
                        break;
                }
            }
            return q;
        }
    }]);