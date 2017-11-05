# -*- coding: utf-8 -*-
# @Author: 胡泽龙
# @Tester：张宏涛
# @File: controlX.py                                                            
# @Time: 2017/10/28                                  
# @Contact: zelonghu@yahoo.com
# @Description: 对于整个system的管理
# @缩紧 空格



"""
1.2

"""
import time
import os
from threading import Timer

error_time = 0
"""
def check_int():
    exit_code = os.system('ping www.baidu.com -c 2')
    if (exit_code):
        print('connection error')
        return 0
    else:
        print('connection success!')
        return 1
    time.sleep(1)
"""
#time适用于定时任务的
def time():
    
    current_time = time.localtime(time.time())
    print(current_time,'new')
    if((current_time.tm_hour == 21) and (current_time.tm_min == 25) and (current_time.tm_sec == 0)):
        print('找到了')

    t=Timer(1,update)
    t.start()

#这里集成了联网检测和最新版本的获取
def pretreatment():
    os.system("sudo rm -f ~/Desktop/project.zip")
    os.system("sudo rm -f -r  ~/Desktop/project")
    if(os.system("sudo wget http://www.nihaocube.cn/project.zip")):
        print('您未联网')
    else:
        print("您已经联网")
    
    os.system("  unzip project.zip  ")
    os.system("  cd project ")

#以下的循环是最主要的循环
if __name__ == '__main__':
    
    pretreatment()
    #update()
    print("初始化程序完成")
    #以下是主程序的运行
    while(True):
        #如果出现失误
        if(os.system("python3 ~/Desktop/project/projcetX.py")):
            print('程序出现错误～')
            error_time = error_time + 1
            if(error_time == 10):
                os.system("sudo reboot")
        

    
#首先测试网络


