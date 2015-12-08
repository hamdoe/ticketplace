'use strict';

app = angular.module('sadminApp');

app.controller('sadminReservationController', ['$scope', 'Reservation',
    function($scope, Reservation){
        $scope.delete  = delete_reservation;
        $scope.waiting = true;

        load_reservations()

        function load_reservations(){
            Reservation.get({depth:3}, // also get contents
                function($response){
                $scope.reservations = $response.objects;
                $scope.waiting = false;
            })
        }

        function delete_reservation(reservation){
            if(! confirm('이 예약을 정말 삭제하시겠습니까? (복구가 불가능합니다.)')){
                return
            }
            $scope.waiting = true;
            Reservation.delete(reservation);
            load_reservations();
        }

    }
])
.filter('reservation_status_filter', function(){
        return function(status){
            return ['예약 신청중', '신청 완료', '신원 확인 완료', '관람완료', '예약 수정 신청중', '예약취소', '예약거절'][status]
        }
    })
.filter('payment_status_filter', function(){
        return function(status){
            return ['결제 되지 않음', '결제 완료', '환불 처리 및 정산 완료'][status]
        }
    });

app.controller('sadminContentController', ['$scope', '$upload', 'TempContent', 'Content', 'Signature',
    function($scope, $upload, TempContent, Content, Signature){

        $scope.checkbox = {}
        $scope.toggle_checkboxes = toggle_checkboxes;
        $scope.master_checkbox = false;
        $scope.files = {}
        $scope.upload = upload;
        $scope.approve = approve;


        load_contents();

        Signature.get(function(response){
            $scope.policy = response.policy;
            $scope.signature = response.signature;
            $scope.access_key = response.access_key;
          });


        function load_contents(){
            TempContent.get(function(result){
                $scope.contents = result.objects;
            })
        }

        function toggle_checkboxes(index_length){
            for(var index=0; index < index_length; index++){
                $scope.checkbox[index] = $scope.master_checkbox;
            }
        }

        function upload(files, content, image_type){
            if(files && files.length){
                var file = files[0];
                var now = new Date();
                var timestamp = ''+now.getFullYear()+'_'+(now.getMonth()+1)+'_'+now.getDate()+'_'+now.getHours()+'_'+now.getMinutes()+'_'+now.getSeconds();
                content[image_type] = image_type + '_' + timestamp+ '_' + file.name;
                $upload.upload({
                    url: 'https://ticketplace.s3.amazonaws.com/', //S3 upload url including bucket name
                    method: 'POST',
                    fields : {
                          key: 'uploads/' + content[image_type], // the key to store the file on S3, could be file name or customized
                          AWSAccessKeyId: $scope.access_key,
                          acl: 'public-read', // sets the access to the uploaded file in the bucket: private or public
                          policy: $scope.policy, // base64-encoded json policy (see article below)
                          signature: $scope.signature, // base64-encoded signature based on policy string (see article below)
                          "Content-Type": file.type != '' ? file.type : 'application/octet-stream' // content type of the file (NotEmpty)
                    },
                    file: file
                });
                var update_query = {content_id: content.content_id};
                update_query[image_type] = content[image_type];
                Content.update(update_query)
            }
        }

        function approve(content){
            $scope.waiting = true;
            Content.update({content_id:content.content_id, status:2}, function(response){
                load_contents()
            })

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
}]).factory('TempContent', ['$resource',
    // sadmin용 임시
    function($resource){
        return $resource('api/temp_content/', {}, {
            get: { method:'GET'}
        });
    }]);