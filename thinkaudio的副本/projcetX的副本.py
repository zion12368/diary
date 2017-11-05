# -*- coding: utf-8 -*-
# @Author: 胡泽龙
# @Tester：张宏涛
# @File: projectX.py                                                            
# @Time: 2017/10/18                                  
# @Contact: zelonghu@yahoo.com
# @Description: 百度语音识别接口调用
"""

7.5



必须的文件。not_get.mp3  ok.mp3  


现在已经出现的error类型：

error001.:没有听到人声，不会退出程序

error_unkonw:其他不成功问题，不会退出程序

unkonwn_error:给后台系统的致命问题

internet connect failed:网络连接问题

say_stop:说了退出

11月3日发现问题：
mp3时常信息读取错误

11月3日更新：
增加了一个提示声音
增加了云端下载功能
修复了第一个字符不知别的bug


10月31日更新：
增加了csr指令文件读入的操作

10月30日更新：
1、无tab化
2、从错误抛出层面写出了联网控制代码
3、中间文件一律放在了shm目录
4、通过在urtelcode里面添加错误处理（重启）机制让声卡资源占用忙的问题得以解决

10月30日讨论问题：
1、声音不够灵敏，远距离听不见
2、硬件的错误处理机制
3、将文件放到shm目录
4、空格化所有
5、开机自启探索


10月27日夜更新：
问题：控制软件应该接受返回值，如果长时间没有返回也需要重启
引入了双麦克轮回录音监控的新系统
加入了识别“魔方”和“模仿”两个字的识别

10月27日更新：

修复了说话的时候触发胰岛素代码的bug


10月26日更新：

增加了一些错误退出机制，但是没有系统支持无法施展拳脚
结局了预处理代码的不停止bug
修复了声音太短而没法剪的bug
下一步改进：调试都是英文化，在人说话后加一个提示音

10月25日夜更新：

我怀着激动的心情发布这一个空前的版本
这个版本集成了两个系统，一个录音，一个检测
这就是我们说的梦幻产品
这个版本删除了以前的非常多的内容，但是留下了我们的技术核心，比如环境监测，比如无按键化，我们通过双麦克风的设计
，完全消灭了间断
24日，我做出了一个版本，但是因为反应太慢（三个子系统同时运转）导致被抛弃，一度陷入空前的抑郁，但是是老张给我了新思路
第二天我整理了新思路，重整旗鼓出发，无奈还是遇到了无法读取没有结束的文件的方法，晚上9点20分我想到了一个把f.wav塞到后面的
奇妙想法，居然奏效了（由此我看出来wav需要一个结尾文件，而这个可以通过添加后缀实现），于是有了现在的版本。

10月23日下午更新：

1、保留了最后一次的录音后再录一段然后提交。
2、把文件读取写入写入了magiccode里面

10月22日夜更新：

1、将动态算法放入了一个循环的后台程序，减少了算法
2、在开始的时候删除所有的缓存文件
3、失败的设置：解决方案，复制一份in-1.wav，并在处理以后删除，主程序储存时也思考这个问题，就可以减少调用

10月21日夜问题整理

问题描述，总是感觉少字，这样处理，先在上传语音识别前，保留最后的十段语音
问题二，七十多个wav都是分析的文件还是什么，为什么会有那么多段（已解决）
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

"""


#注意用sudo vi libso.conf

#执行 sudo ldconfig就可以了。
#重新规划删除无用文件


def reset_file():
    os.system("rm -f conbine.wav")
    os.system("rm -f last.wav")
    os.system("rm -f now_last.wav")
    os.system("rm -f handshake.wav")
    os.system("rm -f in_card2.wav")
    os.system("rm -f in_card1.wav")
    for s in range(0,100):
        os.system(" sudo rm -f /dev/shm/in%d.wav"%s)

import time
import os
import requests 
import eyed3
import wave#用于处理声音
import numpy as np
from threading import Timer
import urllib.request
import urllib
import json
import base64
import time
import pygame
import sys
import string
import re
import csv




VOLUME_GROUP_LEN = 20 #这是语音数组的长度，越大则变化越慢，环境变量越精准

MAX_VOLUME = 1000#这里定义了系统分别人声和环境声音的一个阈值，比这个大的就被认为一定是人声，不会被加入到表中

VOLUME_GAP = 10 #这是处理语音没有识别到人声的一种突发解决方案的间隔

ISOTIMEFORMAT='%a, %d %b %Y %H:%M:%S  '#定义了一种时间样式

CALCULATE_TIMES = 1.3#定义了对于基础音量和帕普庵定义·判断音量的比例

#以下定义了很多的全局变量，在程序里修改调用的时候需要加上global 2017/10/22

REFLASH_SECOENDS = 30 #这里定义了多少次轮魂以后会删除文件保持设备的健康

VERSION = 7.5
print(VERSION)

exit_flag = 0 #这个是用于系统（前台和后台）统一退出的变量

last_flag = 0 #用于引导程序将最后一秒也加上

volume = [] #定义了volume数组

s_average = 0 #average两个是代表了临时的环境音和系统运算出来的环境音

average = 0

record_flag = False #用于指示主程序是不是在录音

kill_flag = 0 #这个 kill_flag 和 bonus_flag  用于胰岛素算法

bonus_flag = 0

record_key = True #这个用于遥控主程序的录音开始

go_times = 0 #用这个来定义已经录音了的时间
#以下是第一种环境音量调节的方法，平均数组法

A_LEN = 20

flag = 0#用于后台判定人声

#判断处理轨迹的计数器
count = 0


a = []#我们的命令代码
#让我们的命令代码变成一个长为A_LEN*12的二维数组
for i  in range(A_LEN):
    a.append([])
    for j in range(12):
        a[i].append(' ')



mode_flag1 = 0#第一声卡的处理flag
mode_flag2 = 1#第二声卡的处理flag


#下面是录音开始结束的时间戳
start_time = time.time()

end_time = time.time()

error_count = 0

def settle_hard_error():
    exit_flag =1
    os.system('sudo reboot')
def check_int():
    return1 = os.system('ping www.taobao.com  -c 2')
    if (return1):
        print ('网络连接不通')
        exit('internet connect failed')
    else:
        print ('网络链接成功')

"""获取wav文件长度"""
def get_length(filename):
    f = wave.open(filename, "rb")
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
    hand_average =average
    f.close()
    print("时间：",b/8000)
    c = b/8000
    return c

"""下面这两个封装代码用于杀死播放程序"""
def get_Pid(process_name):#这段代码可以获取进程的pid码
    cmd = "ps -C %s | grep -v CMD |awk '{ print $1 }'"%(process_name)
    print(cmd)
    pid = os.popen(cmd).read()
    return pid
def kill_arecord(s):
    os.system("sudo kill -9 %s"%(s))

"""用于播放的代码"""
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
"""动态调节的后台环境数组"""
def add_static_volume(a = 0):
    global s_average
    global average
    if(a <= MAX_VOLUME and a > 0):#如果大于600 就一定是人说话或者其他情况
        volume.append(a)
    l = len(volume)

    if (len(volume) > VOLUME_GROUP_LEN):
        del volume[0]
    sum = 0
    for i in volume:
        sum = sum + i
        #如果是第一次调用，那么我们必须要返回一个1，不然没法除
    if(not len(volume)==0):
        return sum / len(volume)
    else:
        return 1

"""预处理文件，作为最开始的初始化代码程序"""
def pretreatment():
    global a

    #将data里面的数据导入到a数组里面
    csvFile = open("/home/pi/Desktop/project/data.csv", "r")
    reader = csv.reader(csvFile)
    count = 0
    for item in reader:
        m = item
        for i in range(len(m)):
            a[count][i] = m[i][2:]
        count = count + 1
    print('读取到的命令数组')
    print(a)

    wait_time = 0

    print("下面开启后台检测程序")

    while(True):

        #print(time.strftime(ISOTIMEFORMAT,time.localtime()),"请说话吧")
        #下面是录音，录一秒
        
        if os.system("sudo arecord -D 'plughw:2,0' -r16000 -f S16_LE -d 1 /dev/shm/in%d.wav"%(wait_time)):
            settle_hard_error()        
                
        


        f = wave.open("/dev/shm/in%d.wav"%(wait_time), "rb")
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
        f.close()
        add_static_volume(average)
        print("现在后台算出的环境音量是",add_static_volume(int(average)))
        wait_time = wait_time + 1

        if(wait_time == 5):
            reset_file()
        
            print("测试音量成功")
            break
        


#我们下一步走向1 的任务
go_flag = 0 

key_to_next = 0  

pid =' '#这里是用来衔接要啥的程序的pid
"""子程序"""
def ultracode():
        #以下是循环代码
    global go_times
    global kill_flag
    global bonus_flag
    global exit_flag 
    global s_average
    global average
    global record_flag
    global flag
    global record_key
    global error_count
    global start_time
    global end_time
    global count
    global mode_flag1 
    global mode_flag2 
    global go_flag
    global key_to_next
    global pid
    global a
    #初始化s_average
    s_average = add_static_volume()

    #计数器加一
    count = count +1 


    #第一件事我们要开始判断这次循环的组态
    #对于变化方向的判断和处理，在中间变量变化的时候删除一些东西，这里
    if(flag == 0):
        if(mode_flag1 == 1 and mode_flag2 == 1 and go_flag == 1 and key_to_next == 1 and flag ==0):
            mode_flag1 = 1
            mode_flag2 = 0
            go_flag = 0
            key_to_next = 0
            
        if(mode_flag1 == 1 and mode_flag2 == 1 and go_flag == 2 and key_to_next ==1 and flag == 0 ):
            mode_flag1 = 0
            mode_flag2 = 1
            go_flag = 0
            key_to_next = 0
            
    if(count % REFLASH_SECOENDS == 0 and flag == 0 ):#每30次并且没有在说话的时候
        if(mode_flag1 == 0 and mode_flag2 == 1 and go_flag == 0):
            mode_flag1 = 1
            mode_flag2 = 1
            go_flag = 1 
            key_to_next = 1

        if(mode_flag1 == 1 and mode_flag2 == 0 and go_flag == 0):
            mode_flag2 = 1
            mode_flag1 = 1
            go_flag = 2
            key_to_next = 1





    #我们约定flag1 就是第一声卡 flag2 就是第二声卡

    print("第一声卡",mode_flag1,"第二声卡",mode_flag2)
    
    #if(mode_flag2 == 0 and flag ==0):#假如是监听音轨并且没有听到人声
        #读取一秒钟的信息，in0 是二号音轨的产生音乐
    if(mode_flag1 == 0):
        if(not pid == ' '):
            kill_arecord(pid)
        if(os.system("sudo arecord -D 'plughw:1,0' -r16000 -f S16_LE  -d 1 /dev/shm/in0.wav")):
            settle_hard_error()
    if(mode_flag2 == 0):
        if(not pid == ' '):
            kill_arecord(pid)
        
        if(os.system("sudo arecord -D 'plughw:2,0' -r16000 -f S16_LE  -d 1 /dev/shm/in0.wav")):
            settle_hard_error()
        #如果处在两个声卡都在录音的时候就复制一个
    if(mode_flag1 == 1 and mode_flag2 == 1):
        #在1 1 时候记录pid 等以后杀了他
        pid = get_Pid('arecord')
        os.system("cp f.wav in0.wav")

    
    
    #计算语音强度average
    f = wave.open("/dev/shm/in0.wav", "rb")
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
    hand_average = average
    f.close()


    #如果没有听到了人声，也就是人没有说话，我才会加进去，这是一种保险，但是一般用不到，因为只会读取in0.wav
    if(average < s_average * CALCULATE_TIMES and average <s_average + 50 and flag == 1):
        s_average = add_static_volume(average)
    else:
        add_static_volume(s_average)#如果有人声，也加自身保证动态

    #以下是胰岛素算法,如果4次都大（小）就给一次胰岛素
    #这是第二种调节方法也就是比例放大缩小
    if(average < s_average and flag ==0):
        kill_flag = kill_flag + 1
        bonus_flag = 0
        if(kill_flag == 3):
            for i in range(1,len(volume)):
                volume[i] = volume[i] * 0.9
            kill_flag = 0


    if(average > s_average and flag == 0):
        bonus_flag = bonus_flag + 1
        kill_flag = 0
        if(bonus_flag == 3):
            for i in range(1,len(volume)):
                volume[i] = volume[i] * 1.5
            bonus_flag = 0



    #如果我们听到了人声，那么我们做个标记
    if(average >= s_average * CALCULATE_TIMES and  average >= s_average + 50):
        print("听到了请您继续说")

        flag = 1#进入了识别

        go_times = go_times + 1#通过这个来看说了几句话

    #如果我们发现没有人声了，然后判断record_flag的值，如果是在录音，咱们给他断了，如果没在录音，就不管他了。

    if(average < s_average * CALCULATE_TIMES or  average < s_average + 50):
        if(flag == 1):

            print("感知到您说话完成")

            #收回录音钥匙以后再停止录音

            record_key = False

            end_time = time.time()#记录现在的时间，用于判断他的时间长度

            #杀死进程
            pid = get_Pid('arecord')
            kill_arecord(pid)


            record_flag = False

            #切割出 从后往前 go_times+3 秒的 wav文件： conbine.wav 播放处理

            #os.system('sox in007.wav f.wav in.wav')#加一秒处理

            wav_len = int(end_time - start_time)

            print('获取的长度:',wav_len)

            print("需要剪切的时间是：",go_times)

            #确定需要文件的名字
            if(mode_flag1 == 0):
                s = '/dev/shm/in_card2.wav'
            if(mode_flag2 == 0):
                s = '/dev/shm/in_card1.wav'

            #如果时间很短，那么直接复制上去的了
            if(wav_len-1-go_times-3 <= 0):
                os.system("cp %s /dev/shm/conbine.wav"%(s))
            else:
                os.system("sox %s /dev/shm/conbine.wav trim %f %f"%(s,wav_len-1-go_times-3,wav_len))

            print("剪切成功")


            s = bdr.getText('/dev/shm/conbine.wav')


           


            if(s == 'error_unknown'):

                print('未知错误')

                error_count = error_count + 1

                pass

            if(s == 'error001'):

                print('没有听清楚')

                pass

            go_times = 0


            print(time.strftime(ISOTIMEFORMAT,time.localtime()),"我：",s)


            #定期处理已经产生的垃圾
            os.system("sudo  rm -f /dev/shm/in0.wav")
            os.system("sudo rm -f /dev/shm/conbine.wav")

            #下面是识别程序的部分

            for i in range(len(a)):
                    if (  (s.find(a[i][5])>=0 and s.find(a[i][6])>=0) ):
                        print("您让我",a[i][1])
                        print("我应该",a[i][11])
            

            if(s.find('魔方')>=0 or s.find('模仿')>=0 ):
                print("听到了我的名字")
                bdr.getVoice('我听到了您说了我的名字','/dev/shm/out.mp3')
                music_play('/dev/shm/out.mp3')
                os.system("rm -f /dev/shm/out.mp3")
                print("下面是新的循环")



            if(s.find('退出')>=0 or s.find('关闭')>=0):
                exit_flag = 1
                print("good bye")
                eixt('say_stop')



            #上面是识别模块的部分

            if(music_play('/home/pi/Desktop/project/duang.mp3')):
                print("提示音播放失误")
                exit_flag = 1
            print("提示音已经播放")


            #用flag标示人的识别代码已经跑完了
            flag = 0

            #用key激活下一次的录音
            start_time = time.time()
            record_key = True

        #如果没有人声也没在录音
        else:
            print("没有听到人声")
            time.sleep(0.1)

    #错误处理
    if(error_count == 100):
        exit('unkonwn_error')


    print("现在的背景音量：",hand_average,"现在的背景音数组:",s_average,"这一次后台计算结束了")

    
    t = Timer(0.1,ultracode)
    t.start()

"""
def send_to_robot(s):
    
    print("请求聊天机器人")
    dic_json = requests.post("http://www.tuling123.com/openapi/api",data={
            "key":"4ee7c2cbfa9749409974ef2aed72bbfc",
            "info":s,
            "userid":"long"
            })
    dic_json=dic_json.json()

    print("机器人：",dic_json['text']) 

    return dic_json['text']
"""

"""百度识别API"""
class BaiduRest:
    def __init__(self, cu_id = 'nihaoku', api_key = "jbY9qOIuiZTqf5ZHrylhGINq", api_secert = '9a70d2e561411592aa8bef22f259791e'):
        
        self.token_url = "https://openapi.baidu.com/oauth/2.0/token?grant_type=client_credentials&client_id=%s&client_secret=%s"
        
        self.getvoice_url = "http://tsn.baidu.com/text2audio?tex=%s&lan=zh&cuid=%s&ctp=1&tok=%s"
       
        self.upvoice_url = 'http://vop.baidu.com/server_api'

        self.cu_id = cu_id

        self.getToken(api_key, api_secert)
        return

    def getToken(self, api_key, api_secert):
        try:
            token_url = self.token_url % (api_key,api_secert)

            r_str = urllib.request.urlopen(token_url).read().decode("utf8")
            token_data = json.loads(r_str)
            self.token_str = token_data['access_token']
            print("获取TOKEN成功")
        except urllib.error.URLError:
            #print(e.message)
            print('监测到没有连接网络')
            exit_flag = 1
            exit('connect error')

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
        
        if(not json.loads(r_data)['err_msg'] == 'success.' and not json.loads(r_data)['err_msg'] == 'speech quality error.'):
            return 'error_unknown'
        res=json.loads(r_data)['result'][0]
        return res 

#首先判断是否联网
#check_int()

bdr = BaiduRest()

if __name__ == '__main__':
    last_record_card = 0
    print('系统加载成功')
    global exit_flag
    global s_average 
    global average
    global record_key
    global record_flag
    global mode_flag1 
    global mode_flag2 
    global go_flag
    global key_to_next
    global start_time
    pretreatment()

    ultracode()
    
    """获取百度的token"""
    
    #以下是预处理方法

    #pretreatment()


    """

    以下是主程序部分，如果想退出那就喊出退出或者关闭，这样可以解决音频设备busy的bug

    """
    
    while(True):
        if(exit_flag == 1):
            eixt(-1)
        if(record_key == True):
            print("下面开始录音")
            record_flag = True
            if(mode_flag1  == 1 and not mode_flag2  == 1):
                last_record_card = 1
                start_time = time.time()
                
                os.system("sudo arecord -D 'plughw:1,0' -r16000 -f S16_LE   /dev/shm/in_card1.wav")
                    
            if(mode_flag2  == 1 and not mode_flag1  == 1):
                last_record_card = 2
                start_time = time.time()
                
                os.system("sudo arecord -D 'plughw:2,0' -r16000 -f S16_LE   /dev/shm/in_card2.wav")
                     
            if(mode_flag1  == 1 and  mode_flag2  == 1 ):
                if(last_record_card == 1):
                    start_time = time.time()#开始的时候记一下时间
                    
                    os.system("sudo arecord -D 'plughw:2,0' -r16000 -f S16_LE   /dev/shm/in_card2.wav")
                        
                    
                if(last_record_card == 2):
                    start_time = time.time()
                
                    os.system("sudo arecord -D 'plughw:1,0' -r16000 -f S16_LE   /dev/shm/in_card1.wav")
                       



            print("录音完成")
        
            
            


       

        #记得重新加入缓存文件处理机制


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
    

        
        

        
        
                               
            

