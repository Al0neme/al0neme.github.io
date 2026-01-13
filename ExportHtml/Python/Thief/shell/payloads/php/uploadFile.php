function uploadFile(){
    $fileName="{{filePath}}";
    $fileContents=base64_decode("{{fileContents}}");
    if (file_put_contents($fileName,$fileContents,FILE_APPEND)!==false){
        return "ok";
    }else{
        return "writer fail";
    }
}
$result=uploadFile();
return $result;