function catFile(){
    $fileName="{{filePath}}";
    return file_get_contents($fileName);
}
$result = base64_encode(catFile());
return $result;