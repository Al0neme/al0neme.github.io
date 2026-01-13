function deleteFile()
{
    $F="{{filePath}}";
    return (file_exists($F)?@unlink($F)?"ok":"fail":"fail");
}

$result = deleteFile();
return $result;