# -*- coding: utf-8 -*-
# @Author: 胡泽龙
# @File: projectX.py                                                            
# @Time: 2017/10/18                                  
# @Contact: zelonghu@yahoo.com
# @Description: 百度语音识别接口调用
"""本版本只是7秒的识别"""
import os
import requests 
import eyed3
import urllib.request
import urllib
import json
import base64
import time
import pygame

api_key = "q1WcDdDRWmXnYnn1aprVislM" 
api_secert = "Q4RCVGVDrrvZXcFN9tx1kOjR2O0c8DsY"

def send_to_robot(s):
    """图灵机器人"""
    print("请求聊天机器人")
    dic_json = requests.post("http://www.tuling123.com/openapi/api",data={
            "key":"4ee7c2cbfa9749409974ef2aed72bbfc",
            "info":s,
            "userid":"long"
            })
    dic_json=dic_json.json()

    print("机器人：",dic_json['text']) 

    return dic_json['text']

def music_play(file = 'out.mp3'):
    #以下是音乐播放
    print("播放音乐out.mp3")

    # 以下获取mp3时间长度

    mp3 =file

    xx=eyed3.load(mp3) 

    mp3_time = xx.info.time_secs

    pygame.mixer.init()

    track = pygame.mixer.music.load(file)
    # 语音播放
    pygame.mixer.music.play()
    #增加一秒钟的播放时间，让它更像真人
    time.sleep(mp3_time+1) 

    pygame.mixer.music.stop()

    print("此次播放完成")


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


 
if __name__ == '__main__':
    print('系统加载成功')

    """获取百度的token"""
    bdr = BaiduRest("test_python", api_key, api_secert)


    while True:
        print("请说话")

        os.system("sudo arecord -D 'plughw:1,0' -r16000 -f S16_LE -d 7 in.wav")
        #s是我们得到的话
        s = bdr.getText("in.wav")

        print("你：",s)

        os.system("rm -f in.wav ")#删除产生的临时文件in.wav

        

        

        if(s=='我没听清楚，请再说一遍'):
            #没有听到的情况，直接调用已经录好的语音
            music_play('not_get.mp3')
        else:
            #以下是音频的获取
            bdr.getVoice(send_to_robot(s),'out.mp3')
            music_play('out.mp3')
            os.system("rm -f out.mp3")#在完成之后删除产生的临时文件out.mp3

        


        
        

        
        
                               
            

