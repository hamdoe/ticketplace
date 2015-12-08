app.controller('emailController', ['$scope', 'Email',
function($scope, Email){
    $scope.send_email = send_email;
    $scope.waiting = false;
    function send_email(){
        $scope.waiting = true;
        Email.send(  {email:'help@ticketplace.net',
        subject:'[문의] ' + $scope.name + '님의 문의사항',
        content: "이름: " + $scope.name + "\n\n이메일: " + $scope.email + "\n\n문의사항 : \n\n" + $scope.content},
            function(response){
                alert('문의사항이 전송되었습니다.')
                $scope.waiting = false;
                $scope.done = true;
            }
        )

    }

}])