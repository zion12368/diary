# -*- coding: utf-8 -*-
import wave
import pylab as pl
import numpy as np
print("import完毕")
# 打开WAV文档

f = wave.open("outtest.wav", "rb")
# 读取格式信息#(nchannels, sampwidth, framerate, nframes, comptype, compname)
params = f.getparams()
nchannels, sampwidth, framerate, nframes = params[:4]
str_data = f.readframes(nframes)
wave_data = np.fromstring(str_data, dtype=np.short)
wave_data.shape = -1, 2
wave_data = wave_data.T
print(wave_data[0])
time = np.arange(0, nframes) * (1.0 / framerate)
print(time )
for i in range(0,len(wave_data[0])):
	print(i,":",wave_data[0][i])
# 绘制波形pl.subplot(211) 
pl.plot(range(25200), wave_data[0])
pl.subplot(212) 
pl.plot(range(25200), wave_data[1], c="g")
pl.xlabel("time (seconds)")
#pl.show()
# 计算平均数
b = len(wave_data[0])
print(b)
sum = 0
for i in range(25200):
	sum = sum + abs(wave_data[0][i])


print(sum/25200)



