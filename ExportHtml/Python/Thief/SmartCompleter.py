from prompt_toolkit import PromptSession
from prompt_toolkit.completion import Completer, Completion
import shlex
from Conf import Conf
from CommonConf import CommonConf

class SmartCompleterMain(Completer):
    # =========================
    # 智能补全器（支持 use 后 Tab 提示）
    # =========================
    def get_completions(self, document, complete_event):
        # 描述（用于补全时显示）
        USE_CONTEXTS, CONTEXT_DESC = CommonConf().GetContext()

        word_before_cursor = document.get_word_before_cursor()
        text_before_cursor = document.text_before_cursor

        # 计算当前词之前的文本
        before_word = text_before_cursor[:-len(word_before_cursor)] if word_before_cursor else text_before_cursor

        # 主命令补全（非 use remove 参数时）
        if not before_word.strip():
            for cmd in Conf.MAIN_COMMAND:
                if cmd.startswith(word_before_cursor):
                    yield Completion(
                        cmd,
                        start_position=-len(word_before_cursor),
                        display_meta=None
                    )
            return

        # 获取当前整行内容
        line = text_before_cursor.strip()
        try:
            parts = shlex.split(line) if line else []
        except ValueError:
            parts = text_before_cursor.split()
        
        # if not parts:
        #     return

        # 处理 use 命令的参数补全
        if parts[0] == 'use':
            for ctx in USE_CONTEXTS:
                if ctx.startswith(word_before_cursor):
                    meta = CONTEXT_DESC.get(ctx, '')
                    yield Completion(
                        ctx,
                        start_position=-len(word_before_cursor),
                        display_meta=meta
                    )

        elif parts[0]=='help':
            for ctx in Conf.SUB_COMMAND:
                if ctx.startswith(word_before_cursor):
                    # meta = Conf.HELP_TEXT_MAIN.get(ctx, '')
                    yield Completion(
                        ctx,
                        start_position=-len(word_before_cursor),
                        # display_meta=meta
                    )
        
        elif parts[0] == 'remove':
            for ctx in USE_CONTEXTS:
                if ctx.startswith(word_before_cursor):
                    meta = CONTEXT_DESC.get(ctx, '')
                    yield Completion(
                        ctx,
                        start_position=-len(word_before_cursor),
                        display_meta=meta
                    )



# =========================
# 子会话专用智能补全器
# =========================

class SubSessionCompleterSub(Completer):
    def get_completions(self, document, complete_event):
        USE_CONTEXTS, CONTEXT_DESC = CommonConf().GetContext()

        word_before_cursor = document.get_word_before_cursor()
        text_before_cursor = document.text_before_cursor

        # 计算当前词之前的文本
        before_word = text_before_cursor[:-len(word_before_cursor)] if word_before_cursor else text_before_cursor

        # 主命令补全（非 use remove 参数时）
        if not before_word.strip():
            for cmd in Conf.SUB_COMMAND:
                if cmd.startswith(word_before_cursor):
                    yield Completion(
                        cmd,
                        start_position=-len(word_before_cursor),
                        display_meta=None
                    )
            return

        # 获取当前整行内容
        line = text_before_cursor.strip()
        try:
            parts = shlex.split(line) if line else []
        except  ValueError:
            parts = text_before_cursor.split()

        # 处理 use 命令的参数补全
        if parts[0] == 'use':
            for ctx in USE_CONTEXTS:
                if ctx.startswith(word_before_cursor):
                    meta = CONTEXT_DESC.get(ctx, '')
                    yield Completion(
                        ctx,
                        start_position=-len(word_before_cursor),
                        display_meta=meta
                    )

        elif parts[0]=='help':
            for ctx in Conf.SUB_COMMAND:
                if ctx.startswith(word_before_cursor):
                    # meta = Conf.HELP_TEXT_MAIN.get(ctx, '')
                    yield Completion(
                        ctx,
                        start_position=-len(word_before_cursor),
                        # display_meta=meta
                    )
        
        elif parts[0] == 'remove':
            for ctx in USE_CONTEXTS:
                if ctx.startswith(word_before_cursor):
                    meta = CONTEXT_DESC.get(ctx, '')
                    yield Completion(
                        ctx,
                        start_position=-len(word_before_cursor),
                        display_meta=meta
                    )