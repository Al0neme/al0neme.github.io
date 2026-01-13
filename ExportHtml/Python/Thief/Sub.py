import shlex
import sys
from prompt_toolkit import PromptSession
from SubCommon import SubCommon
from CommonConf import CommonConf
from SmartCompleter import SubSessionCompleterSub
from Conf import Conf

class BackToMainException(Exception):
    pass

class SubSession:
    # =========================
    # 启动子会话函数
    # =========================
    def start(self,context_name: str,type='',url='',password='',key='',header=''):
        # 使用智能补全器
        session = PromptSession(
            completer=SubSessionCompleterSub(),
            complete_while_typing=True
        )

        print(f"Entered context: {context_name}")

        try:
            while True:
                try:
                    user_input = session.prompt(f"{context_name} > ").strip()
                    if not user_input:
                        continue

                    try:
                        parts = shlex.split(user_input)
                    except ValueError as e:
                        print(f"Args parse error: {e}")
                        continue

                    cmd = parts[0]

                    if cmd == 'back':
                        print("Returning to main menu...")
                        raise BackToMainException()
                    
                    elif cmd == 'add':
                        if len(parts) == 5:
                            SubCommon().add(parts[1], parts[2], parts[3], parts[4])
                        elif len(parts) == 6:
                            SubCommon().add(parts[1], parts[2], parts[3], parts[4], parts[5])
                        else:
                            print(Conf.HELP_TEXT_SUB['add'])

                    elif cmd == 'exit':
                        print("Goodbye!")
                        sys.exit(0)

                    elif cmd == 'help':
                        if len(parts) == 1:
                            SubCommon().show_help()
                        elif len(parts) == 2:
                            SubCommon().show_help(parts[1])
                        else:
                            print(Conf.HELP_TEXT_SUB['help'])

                    elif cmd == 'use':
                        if len(parts) != 2:
                            print(Conf.HELP_TEXT_SUB['use'])
                        else:
                            USE_CONTEXTS, CONTEXT_DESC = CommonConf().GetContext()
                            context_name = parts[1]
                            if context_name not in USE_CONTEXTS:
                                print(f"Unknown context: {context_name}. Choose from:")
                                for ctx in USE_CONTEXTS:
                                    print(f"  {ctx} - {CONTEXT_DESC[ctx]}")
                            else:
                                SHELL_TYPE = CommonConf().GetShellType()
                                url,password,key,header = CommonConf().GetShellConfig(context_name)
                                self.start(context_name,SHELL_TYPE[context_name],url,password,key,header)  # 递归进入下一层
                    elif cmd == 'remove':
                        if len(parts) != 2:
                            print(Conf.HELP_TEXT_SUB['remove'])
                        else:
                            USE_CONTEXTS, CONTEXT_DESC = CommonConf().GetContext()
                            context_name = parts[1]
                            if context_name not in USE_CONTEXTS:
                                print(f"Unknown context: {context_name}. Choose from:")
                                for ctx in USE_CONTEXTS:
                                    print(f"  {ctx} - {CONTEXT_DESC[ctx]}")
                            else:
                                SubCommon().remove(context_name)
                                print("Returning to main menu...")
                                raise BackToMainException()
                    elif cmd == 'generate':
                        if len(parts) != 3:
                            print(Conf.HELP_TEXT_SUB['generate'])
                        else:
                            SubCommon().generate_webshell(parts[1],parts[2])
                            print("shell generated and saved to "+Conf.GENERATE_WEBSHELL_FILEPATH)
                    
                    elif cmd == 'list':
                        SubCommon().list()

                    # =========================
                    # 编写webshell功能调用
                    # start
                    # =========================

                    elif cmd == 'info':
                        if len(parts) == 1:
                            # print("info")
                            # print(type)
                            SubCommon().info(type,url,password,key,header)
                        else:
                            print(Conf.HELP_TEXT_SUB['info'])
                    
                    elif cmd == 'ls':
                        if len(parts) == 1:
                            # print(parts[0])
                            SubCommon().ls(type,url,password,key,header)
                        elif len(parts) == 2:
                            # print(parts[1])
                            SubCommon().ls(type,url,password,key,header,dirName=parts[1])
                        else:
                            print(Conf.HELP_TEXT_SUB['ls'])

                    elif cmd == 'cat':
                        if len(parts) == 2:
                            # print(parts[1])
                            SubCommon().cat_file(type,url,password,key,header,filePath=parts[1])
                        else:
                            print(Conf.HELP_TEXT_SUB['cat'])
                    
                    elif cmd == 'cp':
                        if len(parts) == 3:
                            # print("cp")
                            SubCommon().copy_file(type,url,password,key,header,parts[1],parts[2])
                        else:
                            print(Conf.HELP_TEXT_SUB['cp'])
                    
                    elif cmd == 'mv':
                        if len(parts) == 3:
                            # print("mv")
                            SubCommon().move_file(type,url,password,key,header,parts[1],parts[2])
                        else:
                            print(Conf.HELP_TEXT_SUB['mv'])
                    
                    elif cmd == 'upload':
                        if len(parts) == 3:
                            # print("upload")
                            SubCommon().upload_file(type,url,password,key,header,parts[1],parts[2])
                        else:
                            print(Conf.HELP_TEXT_SUB['upload'])
                    
                    elif cmd == 'rm':
                        if len(parts) == 2:
                            # print("rm")
                            SubCommon().delete_file(type,url,password,key,header,parts[1])
                        else:
                            print(Conf.HELP_TEXT_SUB['rm'])
                    
                    elif cmd == 'execute':
                        if len(parts) != 1:
                            # for i in parts[1:]:
                            #     print(i)
                            SubCommon().execCommand(type,url,password,key,header,parts[1:])
                        else:
                            print(Conf.HELP_TEXT_SUB['execute'])

                    elif cmd == 'settime':
                        if len(parts) == 3:
                            SubCommon().set_file_time(type,url,password,key,header,parts[1],parts[2])
                        else:
                            print(Conf.HELP_TEXT_SUB['settime'])


                    # =========================
                    # end
                    # 编写webshell功能调用
                    # =========================

                    else:
                        print(f"Unknown command: {cmd}. Try 'help'.")

                except KeyboardInterrupt:
                    print("Tip: Use 'back' to return or 'exit' to quit.")
        except BackToMainException:
            raise