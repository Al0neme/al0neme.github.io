import json
import re
import shutil
from typing import List, Optional
from Conf import Conf
import random
import string

class CommonConf:
    def __init__(self):
        pass

    def GetContext(self):
        USE_CONTEXTS = []
        CONTEXT_DESC = {}
        with open(Conf.WEBSHELL_FILE, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                json_obj = json.loads(line)
                # print(json.loads(line))
                USE_CONTEXTS.append(json_obj.get('id'))
                CONTEXT_DESC[json_obj.get('id')] = json_obj.get('url')
            
        return USE_CONTEXTS, CONTEXT_DESC
    
    def GetShellType(self):
        SHELL_TYPE = {}
        with open(Conf.WEBSHELL_FILE, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                json_obj = json.loads(line)
                # print(json.loads(line))
                SHELL_TYPE[json_obj.get('id')] = json_obj.get('type')
        
        return SHELL_TYPE
    
    def GetShellConfig(self,context):
        url = ''
        password = ''
        key = ''
        header = ''
        with open(Conf.WEBSHELL_FILE, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                json_obj = json.loads(line)
                if json_obj.get('id') == context:
                    url = json_obj.get('url')
                    password = json_obj.get('pass')
                    key = json_obj.get('key')
                    header = json_obj.get('header')
        
        return url,password,key,header
                    



    # read webshells and format
    def format_print_webshell_list(self,file_path: str, headers: Optional[List[str]] = None):
        """
        从 JSON Lines 文件中读取数据，并以对齐的表格形式打印。

        参数:
            file_path (str): JSONL 文件路径。
            headers (List[str], optional): 指定字段顺序。若为 None，则使用第一行的键顺序。
        """
        records = []
        
        # 读取并解析文件
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    if line:
                        records.append(json.loads(line))
        except Exception as e:
            print(f"Error: {e}")
            return

        if not records:
            print("文件为空或没有有效 JSON 行。")
            return

        # 确定表头字段
        if headers is None:
            headers = list(records[0].keys())

        # 过滤只包含 headers 中的字段（避免后续 KeyError）
        filtered_records = [
            {key: row.get(key, "") for key in headers}
            for row in records
        ]

        # 计算每列最大宽度（包括表头）
        col_widths = {
            key: max(
                len(str(key)),
                max(len(str(row[key])) for row in filtered_records)
            )
            for key in headers
        }

        # 打印表头
        header_line = "  ".join(f"{key:<{col_widths[key]}}" for key in headers)
        print("-" * len(header_line))
        print(header_line)
        print("-" * len(header_line))

        # 打印数据行
        for row in filtered_records:
            row_line = "  ".join(f"{str(row[key]):<{col_widths[key]}}" for key in headers)
            print(row_line)


    def generateID(self):
        # 定义字符集：数字 + 小写字母
        charset = string.digits + string.ascii_lowercase  # '0123456789abcdefghijklmnopqrstuvwxyz'

        # 生成8位随机字符串
        webshell_ID = ''.join(random.choices(charset, k=8))

        return webshell_ID

    def remove_webshell(self,file_path, target_string, backup=True):
        if backup:
            shutil.copy2(file_path, file_path + '.bak')  # 创建备份

        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        new_lines = [line for line in lines if target_string not in line]

        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)

    # php getFileAtt func result format
    def format_result_php_getFileAtt(self, data):
        """
        格式化目录数据为紧凑对齐表格，无多余空行。
        新增 Attr 列显示权限（如 RWX），DIR 类型 Size 不显示。
        """
        dir_path = data.get('Dir', 'Unknown')
        count = data.get('count', 0)

        # 提取数据行：name, is_dir_flag, modified, size, attr
        rows = []
        for k in sorted((k for k in data.keys() if k.isdigit()), key=int):
            name, is_dir_flag, modified, size, attr = data[k]
            file_type = "DIR" if is_dir_flag == '0' else "FILE"

            # 只有 FILE 显示大小，DIR 的 Size 留空
            if file_type == "FILE":
                try:
                    size_val = int(size)
                    size_str = f"{size_val:,}"
                except (ValueError, TypeError):
                    size_str = ""
            else:
                size_str = ""

            # 权限字段直接使用 PHP 返回的 attr（如 "RWX"）
            perm_str = str(attr).strip() if attr else "---"

            rows.append([name, size_str, modified, file_type, perm_str])

        # 构建输出行
        lines = [
            f"Directory: {dir_path}",
            f"Total Items: {count}"
        ]

        if not rows:
            lines.append("No items.")
            return '\n'.join(lines)

        # 表头与列宽（Name, Size, Modified, Type, Attr）
        headers = ["Name", "Size", "Modified", "Type", "Attr"]
        col_widths = [
            max(len(row[i]) for row in rows + [headers])
            for i in range(5)  # 5 列
        ]

        # 构造表头行（Size 右对齐，其余左对齐）
        header_line = (
            headers[0].ljust(col_widths[0]) +
            '  ' +
            headers[1].rjust(col_widths[1]) +  # Size 右对齐
            '  ' +
            headers[2].ljust(col_widths[2]) +
            '  ' +
            headers[3].ljust(col_widths[3]) +
            '  ' +
            headers[4].ljust(col_widths[4])
        )

        separator = "-" * len(header_line)

        # 拼接结果
        lines.append(separator)
        lines.append(header_line)
        lines.append(separator)

        # 添加数据行
        for row in rows:
            line = (
                row[0].ljust(col_widths[0]) +
                '  ' +
                row[1].rjust(col_widths[1]) +  # Size 右对齐（空字符串也占位）
                '  ' +
                row[2].ljust(col_widths[2]) +
                '  ' +
                row[3].ljust(col_widths[3]) +
                '  ' +
                row[4].ljust(col_widths[4])  # Attr 左对齐
            )
            lines.append(line)

        return '\n'.join(lines)


    def format_result_jsp_getFileAtt(self,data: str) -> str:
        """
        解析服务器返回的自定义格式文件列表，并格式化为对齐表格。

        支持字段：
            Name（左对齐）、Size（右对齐，仅文件显示）、Modified、Type、Attr（如 RWX）
        目录的 Size 留空，文件大小带千分位逗号。
        
        参数:
            data (str): 来自 requests 的 .text 响应内容
        
        返回:
            str: 格式化的多行字符串
        """
        # Step 1: 修复单反斜杠导致的 \uXXXX 错误（如 c:\users\public → c:\\users\\public）
        fixed_text = re.sub(r'(?<!\\)\\(?!\\)', r'\\\\', data)

        # 解析 JSON
        try:
            data = json.loads(fixed_text)
        except json.JSONDecodeError as e:
            raise ValueError(f"JSON 解析失败: {e}")

        # 获取当前目录
        current_dir = data.get("currentDir", "./").replace("\\\\", "\\")

        # 构建文件数据列表
        files = []
        index = 0
        while str(index) in data:
            raw_entry = data[str(index)]
            if not isinstance(raw_entry, str) or not raw_entry.startswith("{") or not raw_entry.endswith("}"):
                index += 1
                continue

            # 提取 {key=value} 对
            inner = raw_entry[1:-1]  # 去掉 {}
            pairs = [p.strip() for p in inner.split(",")]
            item = {}

            for pair in pairs:
                if "=" not in pair:
                    continue
                k, v = pair.split("=", 1)
                try:
                    key = int(k.strip())
                    value = v.strip()
                    item[key] = value
                except ValueError:
                    pass  # 忽略无效键

            # 映射字段
            name = item.get(0, "unknown")
            is_file_flag = item.get(1, "0")
            modified = item.get(2, "")
            size_str = item.get(3, "0")
            attr = item.get(4, "") or "---"  # 默认值

            file_type = "FILE" if is_file_flag == "1" else "DIR"

            # 文件才显示大小
            size_display = ""
            if file_type == "FILE":
                try:
                    size_val = int(size_str.replace(",", ""))
                    size_display = f"{size_val:,}"
                except ValueError:
                    size_display = ""

            files.append({
                "name": name,
                "size": size_display,
                "modified": modified,
                "type": file_type,
                "attr": attr
            })
            index += 1

        # =============================
        #   构建格式化输出字符串
        # =============================

        output_lines = []

        # 基本信息
        output_lines.append(f"Directory: {current_dir}")
        output_lines.append(f"Total Items: {len(files)}")

        if len(files) == 0:
            return "\n".join(output_lines)

        # 表头定义
        headers = ["Name", "Size", "Modified", "Type", "Attr"]

        # 计算每列最大宽度（兼容表头和所有行）
        col_widths = [
            max(
                len(row[i]) for row in [
                    [f["name"], f["size"], f["modified"], f["type"], f["attr"]]
                    for f in files
                ] + [[h, "", "", "", ""] for h in headers]
            )
            for i in range(5)
        ]

        # 构造表头行（Size 右对齐，其余左对齐）
        header_line_parts = [
            headers[0].ljust(col_widths[0]),
            headers[1].rjust(col_widths[1]),  # Size 右对齐
            headers[2].ljust(col_widths[2]),
            headers[3].ljust(col_widths[3]),
            headers[4].ljust(col_widths[4])
        ]
        header_line = "  ".join(header_line_parts)

        separator = "-" * len(header_line)

        # 拼接输出
        output_lines.append(separator)
        output_lines.append(header_line)
        output_lines.append(separator)

        # 添加每一行数据
        for f in files:
            line_parts = [
                f["name"].ljust(col_widths[0]),
                f["size"].rjust(col_widths[1]),      # 右对齐保持列整齐
                f["modified"].ljust(col_widths[2]),
                f["type"].ljust(col_widths[3]),
                f["attr"].ljust(col_widths[4])
            ]
            output_lines.append("  ".join(line_parts))

        return "\n".join(output_lines)
    
    def format_result_aspx_getFileAtt(self,json_str):
        """
        将指定格式的 JSON 字符串转换为对齐的文件列表表格（字符串形式返回）

        :param json_str: 输入的 JSON 字符串
        :return: 格式化后的字符串表格
        """
        json_str = json_str.replace('\\','\\\\')
        try:
            data = json.loads(json_str)
        except Exception as e:
            return "Error: Invalid JSON - " + str(e)

        # 提取条目，排除 'count' 和 'currentDir'
        entries = [v for k, v in data.items() if k not in ['count', 'currentDir']]

        # 按原始键排序：确保顺序是 0,1,2,...
        try:
            sorted_keys = sorted((int(k), v) for k, v in data.items() if k not in ['count', 'currentDir'])
            sorted_entries = [item for key, item in sorted_keys]
        except ValueError:
            # 如果键无法转为 int，则按原顺序
            sorted_entries = entries

        # 构建输出字符串
        lines = []
        lines.append("-" * 60)
        lines.append(f"{'Name':<20} {'Size':>6}  {'Modified':<16} {'Type':<4}  {'Attr'}")
        lines.append("-" * 60)

        def format_size(size_bytes):
            size = int(size_bytes)
            if size < 1024:
                return f"{size}B"
            else:
                return f"{size / 1024:.1f}K"

        for item in sorted_entries:
            name = next((i["name"] for i in item if "name" in i), "Unknown")
            size = next((i["size"] for i in item if "size" in i), "0")
            dt = next((i["datetime"] for i in item if "datetime" in i), "")
            is_file = next((i["is_file"] for i in item if "is_file" in i), "0")
            perm = next((i["permission"] for i in item if "permission" in i), "---")

            ftype = "FILE" if is_file == "1" else "DIR"
            formatted_size = format_size(size)

            line = f"{name:<20} {formatted_size:>6}  {dt:<16} {ftype:<4}  {perm}"
            lines.append(line)

        # 将所有行合并为一个字符串并返回
        return "\n".join(lines)