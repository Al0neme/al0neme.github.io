# main.py - 主会话模块

from prompt_toolkit import PromptSession
import shlex
import sys
from SmartCompleter import SmartCompleterMain
from MainCommon import MainCommon
from CommonConf import CommonConf
from Conf import Conf

# =========================
# 主函数
# =========================

def main():
    # 使用智能补全器
    session = PromptSession(
        completer=SmartCompleterMain(),
        complete_while_typing=True  # 实时补全
    )

    print("Thief started. Type 'help' for commands.")

    while True:
        try:
            user_input = session.prompt('> ').strip()
            if not user_input:
                continue

            try:
                parts = shlex.split(user_input)
            except ValueError as e:
                print(f"Args parse error: {e}")
                continue

            cmd = parts[0]

            if cmd == 'exit':
                print("Goodbye!")
                sys.exit(0)

            elif cmd == 'help':
                if len(parts) == 1:
                    MainCommon().show_main_help()
                elif len(parts) == 2:
                    MainCommon().show_main_help(parts[1])
                else:
                    print(Conf.HELP_TEXT_MAIN['help'])

            elif cmd == 'use':
                if len(parts) != 2:
                    print(Conf.HELP_TEXT_MAIN['use'])
                else:
                    context_name = parts[1]
                    USE_CONTEXTS, CONTEXT_DESC = CommonConf().GetContext()
                    if context_name not in USE_CONTEXTS:
                        print(f"Unknown context: {context_name}. Choose from:")
                        for ctx in USE_CONTEXTS:
                            print(f"  {ctx} - {CONTEXT_DESC[ctx]}")
                    else:
                        print(f"Starting enter: {context_name}")
                        SHELL_TYPE = CommonConf().GetShellType()
                        MainCommon().start_subsession(context_name,type=SHELL_TYPE[context_name])

            elif cmd == 'add':
                if len(parts) == 5:
                    MainCommon().add(parts[1], parts[2], parts[3], parts[4])
                elif len(parts) == 6:
                    MainCommon().add(parts[1], parts[2], parts[3], parts[4], parts[5])
                else:
                    print(Conf.HELP_TEXT_MAIN['add'])

            elif cmd == 'list':
                MainCommon().list()

            elif cmd == 'remove':
                if len(parts) != 2:
                    print(Conf.HELP_TEXT_MAIN['remove'])
                else:
                    context_name = parts[1]
                    USE_CONTEXTS, CONTEXT_DESC = CommonConf().GetContext()
                    if context_name not in USE_CONTEXTS:
                        print(f"Unknown context: {context_name}. Choose from:")
                        for ctx in USE_CONTEXTS:
                            print(f"  {ctx} - {CONTEXT_DESC[ctx]}")
                    else:
                        MainCommon().remove(context_name)
            
            elif cmd == 'generate':
                if len(parts) != 3:
                    print(Conf.HELP_TEXT_MAIN['generate'])
                else:
                    MainCommon().generate_webshell(parts[1],parts[2])
                    print("shell generated and saved to "+Conf.GENERATE_WEBSHELL_FILEPATH)

            else:
                print(f"Unknown command: {cmd}. Try 'help'")

        except KeyboardInterrupt:
            print("Use 'exit' to quit.")
        except EOFError:
            print("Goodbye!")
            sys.exit(0)
        except Exception as e:
            if isinstance(e, SystemExit):
                raise
            print(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()