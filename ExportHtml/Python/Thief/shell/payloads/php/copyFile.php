function copyFile(){
    $srcFileName="{{srcFileName}}";
    $destFileName="{{destFileName}}";
    if (@is_file($srcFileName)){
        if (copy($srcFileName,$destFileName)){
            return "ok";
        }else{
            return "fail";
        }
    }else{
        return "The target does not exist or is not a file";
    }
}
$result = copyFile();
return $result;