function setFileTime(){

    $filename = '{{filename}}';
    $result = '';
    if (file_exists($filename)) {
        $currentMtime = filemtime($filename);
        $currentAtime = fileatime($filename);

        $newMtime = "{{newMtime}}";
        $newAtime = "{{newAtime}}";

        if (touch($filename, strtotime($newMtime), strtotime($newAtime))) {
            $result .= "history modified time: " . date("Y-m-d H:i:s", $currentMtime) . "\n";
            $result .= "history accessed time: " . date("Y-m-d H:i:s", $currentAtime) . "\n";
            $result .= "new modified time: " . date("Y-m-d H:i:s", strtotime($newMtime)) . "\n";
            $result .= "new accessed time: " . date("Y-m-d H:i:s", strtotime($newAtime)) . "\n";
        } else {
            $result .= "can not update timestamp\n";
        }
    } else {
        $result .= "'$filename' is not exist\n";
    }
    return $result;

}

$result = setFileTime();
return $result;