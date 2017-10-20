# -*- coding: utf-8 -*-
import urllib.request
import urllib
import json
import base64
api_key = "q1WcDdDRWmXnYnn1aprVislM" 
api_secert = "Q4RCVGVDrrvZXcFN9tx1kOjR2O0c8DsY"
class BaiduRest:
    def __init__(self, cu_id, api_key, api_secert):
        
        self.token_url = "https://openapi.baidu.com/oauth/2.0/token?grant_type=client_credentials&client_id=%s&client_secret=%s"
        
        self.getvoice_url = "http://tsn.baidu.com/text2audio?tex=%s&lan=zh&cuid=%s&ctp=1&tok=%s"
       
        self.upvoice_url = 'http://vop.baidu.com/server_api'

        self.cu_id = cu_id
        self.getToken(api_key, api_secert)
        return

    def getToken(self, api_key, api_secert):
        
        token_url = self.token_url % (api_key,api_secert)

        r_str = urllib.request.urlopen(token_url).read().decode("utf8")
        token_data = json.loads(r_str)
        self.token_str = token_data['access_token']
        pass

    def getVoice(self, text, filename):
        print("准备开始请求音频")

        get_url = self.getvoice_url % (urllib.parse.quote(text), self.cu_id, self.token_str)

        voice_data = urllib.request.urlopen(get_url).read()

        print("返回成功")
        voice_fp = open(filename,'wb+')
        voice_fp.write(voice_data)
        voice_fp.close()
        pass

    def getText(self, filename):
        print("准备开始请求识别")
        data = {}
        
        data['format'] = 'wav'
        data['rate'] = 16000
        data['channel'] = 1
        data['cuid'] = self.cu_id
        data['token'] = self.token_str
        wav_fp = open(filename,'rb')
        voice_data = wav_fp.read()
        data['len'] = len(voice_data)
        data['speech'] = base64.b64encode(voice_data).decode('utf-8')
        post_data = json.dumps(data)
        r_data = urllib.request.urlopen(self.upvoice_url,data=bytes(post_data,encoding="utf-8")).read().decode("utf8")
        print("返回成功")
        print(json.loads(r_data)['err_msg'])
        if(json.loads(r_data)['err_msg'] == 'speech quality error.'):
            return "我没听清楚，请再说一遍"
        res=json.loads(r_data)['result'][0]
        return res 


print('系统加载成功')

"""获取百度的token"""
bdr = BaiduRest("9672208", api_key, api_secert)
bdr.getVoice('抱歉，我没有听清楚',"not_get.mp3")