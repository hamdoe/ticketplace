'use strict';

app.controller('noticeListController', ['$scope', 'Notice', '$route', '$location',
  function($scope, Notice, $route, $location) {
      Notice.query(function($response){
          $scope.notices = $response.objects;
      })
  }]);
app.controller('noticeViewController', ['$scope', 'Notice', '$routeParams', '$location',
  function($scope, Notice, $routeParams, $location) {
      var notice_id = Number($routeParams.notice_id);
      $scope.notice = Notice.get({notice_id:notice_id}, function(response){
          Notice.update({notice_id:notice_id, view_count: $scope.notice.view_count+1 });
      });

      var last_post_query = {"filters":[{"name":"notice_id","op":"<","val":notice_id}],"order_by":[{"field":"notice_id","direction":"desc"}], "limit":1};
      var next_post_query = {"filters":[{"name":"notice_id","op":">","val":notice_id}],"order_by":[{"field":"notice_id"}], "limit":1};
      Notice.get({q:last_post_query}, function(response){
          if(response.num_results === 0){
              $scope.last_post = null
          }else{
              $scope.last_post = response.objects[0];
          }
      });
      Notice.get({q:next_post_query}, function(response){
          if(response.num_results === 0){
              $scope.next_post = null
          }else{
              $scope.next_post = response.objects[0];
          }
      });
  }]);
app.controller('reservationNewController', ['$scope', 'Reservation', '$route', '$location',
  function($scope, Reservation, $route, $location) {
  }]);