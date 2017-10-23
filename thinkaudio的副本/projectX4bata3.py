# -*- coding: utf-8 -*-
# @Author: 胡泽龙
# @File: projectX.py                                                            
# @Time: 2017/10/18                                  
# @Contact: zelonghu@yahoo.com
# @Description: 百度语音识别接口调用
"""

本版本集成了分段的技术，并且支持退出和关闭指令，在封装方面还没有做的很好，仅供测试使用
现在已经出现的error类型：
error001:没有听到人声

10月21日夜问题整理
问题描述，总是感觉少字，这样处理，先在上传语音识别前，保留最后的十段语音
问题二，七十多个wav都是分析的文件还是什么，为什么会有那么多段
好消息，我申请的百度语音账号已经授权无限期无次数限制，可以多台一起搞了
问题三，如果两秒钟的语音录音没问题了，解决了问题一，就还变成一秒一次比较好，目前延时变高了一点点
问题四，还是有长时间连续发音的时候他认为太长了导致程序出错而退出，从而我判断，有很多种错误都要分别进行处理，超过十秒则完全忽略词句并提高空间噪声值域
问题五、自己重启系统并且删除缓存
10月21日晚上更新：
1、新加入了动态调节机制，调节环境音量
2、去掉了图灵机器人的调用
3、简化了运算流程，识别率大大提升
4、定义环境变量数组的值为20，太多了增加很多计算，目前算法很强不用那么多的数组
5、增加了一个语音出发的条件，那就是要比环境音至少多50，防止出现个位数和个位数比较还在录音的bug

10月21日下午更新：
1、对于没有成生的speech quality error有了一种解决方法，一旦用户产生了speech quality error 那么就会对环境变量加10
*2、解决了环境检测问题。目前只有一个40个变量的数组，具体调试在开始的宏设置。


10月21日上午更新：
1、增加了保留上一段录音机制
2、预处理代码函数化

没有解决的问题：
1、自己重启机制
2、中间文件缓存处理机制,根目录缺失，程序会在目录里产生很多很多的音频文件
3、AI模块设计，接口设计，网络结构的设计
4、封装的研究
5、看一下百度的错误列表
6、并没有拿掉预处理阶段，因为这需要给那个环境音量数组提供最开始的数据，胡认为应该保留
7、在语音播放完后会有一个小延迟，这个时候如果客户说话就会录不进去了
8、麦克风太远了不行，太原了就听不清楚了
"""


"""Debian/Ubuntu
以下是pyaudio的安装//目前没用
Use the package manager to install PyAudio:

sudo apt-get install python-pyaudio python3-pyaudio
If the latest version of PyAudio is not available, install it using pip:

pip3 install pyaudio
Notes:

pip will download the PyAudio source and build it for your system. Be sure to install the portaudio library development package (portaudio19-dev) and the python development package (python-all-dev) beforehand.
For better isolation from system packages, consider installing PyAudio in a virtualenv.


以下是eyed3 的安装//用于获取语音长度
pip3 install eyeD3


以下是sox命令软件的安装//用于语音的拼接
1.下载SOX

sox-14.4.1.tar.gz

2.安装sox文件

　　1）解压　　tar -zxvf sox-14.4.1.tar.gz

　　2）进入sox14.4.1目录中执行./configure

　　3）执行 make命令

　　4）执行make install命令m
错误的现象：

 Sox error while loading shared libraries: libsox.so.2: cannot open shared object file: No such file

 

问题原因：在/usr/local/lib当中是有libsox.so.2,只不过是找不到而已。

在 /etc/ld.so.conf.d 目录当中创建一个文件，libso.conf：加入

/usr/local/lib/libsox.so.2.
注意用sudo vi libso.conf

执行 sudo ldconfig就可以了。


"""
import time
import os
import requests 
import eyed3

import wave#用于处理声音

import numpy as np

import urllib.request
import urllib
import json
import base64
import time
import pygame

VOLUME_GROUP_LEN = 20 #这是语音数组的长度，越大则变化越慢，环境变量越精准

MAX_VOLUME = 1000#这里定义了系统分别人声和环境声音的一个阈值，比这个大的就被认为一定是人声，不会被加入到表中

VOLUME_GAP = 10 #这是处理语音没有识别到人声的一种突发解决方案的间隔

ISOTIMEFORMAT='%a, %d %b %Y %H:%M:%S  '#定义了一种时间样式

CALCULATE_TIMES = 1.3#定义了对于基础音量和帕普庵定义·判断音量的比例

api_key = "q1WcDdDRWmXnYnn1aprVislM"

api_secert = "Q4RCVGVDrrvZXcFN9tx1kOjR2O0c8DsY"


volume = []#定义了volume数组

#以下是第一种环境音量调节的方法，平均数组法
def add_static_volume(a = 0):

    if(a <= MAX_VOLUME and a > 0):#如果大于600 就一定是人说话或者其他情况
        volume.append(a)
    l = len(volume)

    if (len(volume) > VOLUME_GROUP_LEN):
        del volume[0]
    sum = 0
    for i in volume:
        sum = sum + i
        
    return sum / l



def reset_file():
    
    os.system("rm -f conbine.wav")
    os.system("rm -f last.wav")
    for s in range(0,100):
        os.system("rm -f in%d.wav"%s)



def add_all_inwav(n):
    node_string=' '
    main_string = []
    for i in range(n):
        main_string.append('in%d.wav'%(i))

    return node_string.join( main_string )


def pretreatment():
    wait_time = 0
    FAVERAGE = 0
    reset_file()

    while(True):
        

    
        #print(time.strftime(ISOTIMEFORMAT,time.localtime()),"请说话吧")
        #下面是录音，录一秒
        
        os.system("sudo arecord -D 'plughw:1,0' -r16000 -f S16_LE -d 1 in%d.wav"%(wait_time))

        
        f = wave.open("in%d.wav"%(wait_time), "rb")
        # 读取格式信息#(nchannels, sampwidth, framerate, nframes, comptype, compname)
        params = f.getparams()
        nchannels, sampwidth, framerate, nframes = params[:4]

        str_data = f.readframes(nframes)
        wave_data = np.fromstring(str_data, dtype=np.short)
        wave_data.shape = -1, 2
        wave_data = wave_data.T

        
        # 计算单个平均数
        sum = 0

        b = len(wave_data[0])
        for i in range(b):
            sum = sum + abs(wave_data[0][i])
            average = sum / b

        print("现在后台算出的环境音量是",add_static_volume(int(average)))

        FAVERAGE  = FAVERAGE + average;#求average的平均

        print(time.strftime(ISOTIMEFORMAT,time.localtime()),"结果：",average)

        wait_time = wait_time + 1 #这一次加一

        if(wait_time == 5):

            FAVERAGE = FAVERAGE / 5#求出了最终平均数
            print("测试音量成功")
            print("静音声音是：",FAVERAGE,"超过的视为说话")
            f.close()
            return FAVERAGE


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
            #这里是没听到人声的处理方法，如果及其嘈杂的环境，则会让volume所有的都增加20的数值，直到不出现这种情况，
            #假如出现误判，那么也会在add_static_volume中被矫正，这段代码是用于及其特殊的情况的，比如狗叫、猫叫，在以后的一段时间屏蔽
            for i in range(1,len(volume)):
                volume[i] = volume[i] + VOLUME_GAP
            return "error001"
        res=json.loads(r_data)['result'][0]
        return res 


 
if __name__ == '__main__':


    print('系统加载成功')
    
    """获取百度的token"""
    bdr = BaiduRest("test_python", api_key, api_secert)

    STATUS_AVERAGE = 0#STATUS_AVERAGE 是预处理中的环境分贝量

    wait_time = 0#wait_time 是我们等待的次数

    print("测试时间5秒, 请耐心等待")

    #以下是预处理方法

    STATUS_AVERAGE = pretreatment()


    """

    以下是主程序部分，如果想退出那就喊出退出或者关闭，这样可以解决音频设备busy的bug

    """
    lastwav_exist_flag = False#first_flag 表示有没有last。wav的存在
    kill_flag = 0
    bonus_flag = 0
    while True:

        #第一层循环是一句话一句话的循环，每一次循环会产生一句话

        wait_time = 0

        while(True):
            # 第二层循环是抓取音频并在退出的时候产生一个combine.wav 的合成音频文件

            #suprint(time.strftime(ISOTIMEFORMAT,time.localtime()),"请说话吧")

            #下面是录音，录一秒

            os.system("sudo arecord -D 'plughw:1,0' -r16000 -f S16_LE -d 1 in%d.wav"%(wait_time))
            #对于这一秒信息计算求平均数，



            f = wave.open("in%d.wav"%(wait_time), "rb")

            # 读取格式信息#(nchannels, sampwidth, framerate, nframes, comptype, compname)
            params = f.getparams()
            nchannels, sampwidth, framerate, nframes = params[:4]
            str_data = f.readframes(nframes)
            wave_data = np.fromstring(str_data, dtype=np.short)
            wave_data.shape = -1, 2
            wave_data = wave_data.T
            # 计算平均数
            sum = 0
            b = len(wave_data[0])
            for i in range(b):
                sum = sum + abs(wave_data[0][i])
            average = sum / b
            print("结果：",average)
            f.close()

            s_average = add_static_volume()

            #如果听到了人声
            if(average < s_average * CALCULATE_TIMES and average <s_average + 50 and wait_time > 0):
                s_average = add_static_volume(average)


            #以下是胰岛素算法,如果6次都大（小）就给一次胰岛素
            #这是第二种调节方法也就是比例放大缩小
            if(average < s_average):
                kill_flag = kill_flag + 1
                bonus_flag = 0
                if(kill_flag == 5):
                    for i in range(1,len(volume)):
                        volume[i] = volume[i] * 0.9
                    kill_flag = 0


            if(average > s_average):
                bonus_flag = bonus_flag + 1
                kill_flag = 0
                if(bonus_flag == 5):
                    for i in range(1,len(volume)):
                        volume[i] = volume[i] * 1.5
                    bonus_flag = 0


            print("现在后台算出的环境音量是",s_average)


            wait_time = wait_time + 1#计数器加一

            #以下是发现出现静音并处理,如果没有静音，继续录，如果没出现声音，分两种情况，一直没有声音执行，和说完了
            if(average < s_average * CALCULATE_TIMES or average < s_average + 50):#这是没有声音的情况,如果超过了1.5倍的静音音量和比平静音高50就算是则证明在说话
                
                if(wait_time >1):#如果有多个文件,那么证明是一句话，把他们叠加起来，然后进入后面的系统

                    if(lastwav_exist_flag == True):

                        os.system("sox last.wav %s conbine.wav"%(add_all_inwav(wait_time -1)))
                    else:
                        os.system("sox  %s conbine.wav"%(add_all_inwav(wait_time -1)))

                    print("成功输出了一个")

                    for i in range(0,wait_time -2):#这是清扫代码，目的在于清除产生的废品
                        os.system("rm -f in%d.wav"%(i))

                    break#跳入到了语音识别播放代码

                else:#如果只是一次的话,输出一句您好象没有说话。

                    print("您好像没说话")

                    os.system("mv -f in%d.wav last.wav"%(wait_time-1))#将上一个保存到last。wav里面

                    lastwav_exist_flag = True#判定不是第一句了

                    wait_time = 0

                    continue;

            
            else:#这是有声音的情况，继续滚动直到没有声音为止
                continue



        """
        conbine.wav语音提取成功
        以下是我们的识别模块和语音合成模块

        """
        

        s = bdr.getText("conbine.wav")#s是我们得到的话


        print("你：",s)

        #这是我们识别模块，已经集成了退出功能
        if( s.find('关闭') >= 0 or s.find('退出') >= 0):
            exit(-1)



        os.system("rm -f conbine.wav ")#删除产生的临时文件in.wav

        #bdr.getVoice('好的知道了','out.mp3')

        music_play('out.mp3')

        if(wait_time == 100):
            reset_file()


        """
        if(s=='error001'):
            #没有听到的情况，直接调用已经录好的语音
            continue
        else:
            #以下是音频的获取
            bdr.getVoice(s,'out.mp3')
            music_play('out.mp3')
            os.system("rm -f out.mp3")#在完成之后删除产生的临时文件out.mp3

        """
    

        
        

        
        
                               
            

