function moveFile(){
    $srcFileName="{{srcFileName}}";
    $destFileName="{{destFileName}}";
    if (rename($srcFileName,$destFileName)){
        return "ok";
    }else{
        return "fail";
    }

}

$result = moveFile();
return $result;