print("现在的背景音量：",average,"现在的背景音数组:",s_average)
#这是我们识别模块，已经集成了退出功能
        if(s.find('关闭') >= 0 or s.find('退出') >= 0):
            exit_flag = 1
            exit(-1

os.system("cat attach.wav in007.wav > conbine.wav")
        s = bdr.getText("conbine.wav") #s是我们得到的话
        print("你：",s)
        if(s == 'error001' or s == 'error_unknown'):
            break


#以下是并行运算程序，在后台运行，负责时时计算现在的音量和背景音量
def calculate_volume():
    global kill_flag
    global bonus_flag
    global exit_flag 
    global s_average
    global average
    
    global arecord_go 
    global hand_average
    average = add_static_volume()
    if(os.path.exists('handshake.wav')==True):
        print("循环一次运算代码")
        f = wave.open("handshake.wav", "rb")

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

        #以下是对于背景音量的运算
        os.system("rm -f handshake.wav")
        #如果没有听到了人声，也就是人没有说话，我才会加进去，这是一种保险，但是一般用不到，因为只会读取in0.wav
        if(average < s_average * CALCULATE_TIMES and average <s_average + 50 ):
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
        if(exit_flag == 1):
            exit(-1)
        
        #循环代码结束
    if(hand_average >= s_average * CALCULATE_TIMES and  hand_average >= s_average + 50):
        arecord_go = 1
        os.system("cp in1.wav attach.wav")

    t = Timer(0.01,calculate_volume)
    t.start()