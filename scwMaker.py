import math
import wave
import struct
import matplotlib.pyplot as plt
import numpy as np
import random as rand

audio = []
sampleRate = 44100.0
saveFile = "Waveforms/output.wav"
msam = 0.0

def myWave(sample):
    lsam = 0
    temp = 0
    harm = 1
    while harm < 2**16:
        #lsam += math.cos(math.tan(harm*sample/harm**0.5 - math.sin(math.tan(harm**0.1))/harm**0.5))*math.sin(harm*sample/2 + math.tan(4*harm))/harm**2
        #lsam += math.sin(sample*(harm**(1.5+math.cos(harm/math.pi))))/harm**2.3
        #lsam += math.atan(math.sin(sample*harm)*200/harm)/harm**2 - math.sin(harm*sample)/harm**2
        lsam += math.sin(harm*sample)/harm**2
        harm = harm + math.sqrt(harm)
    return lsam

def generate_wave(volume=0.5):

    global audio, msam

    for x in range(0,2696):
        sample = 2 * math.pi * 16.351 * ( x / sampleRate )
        temp = volume * myWave(sample)
        if abs(temp) > abs(msam):
            msam = temp
        audio.append(temp)
        if x == 674:
            print("25% Complete")
        elif x == 1348:
            print("50% Complete")
        elif x == 2022:
            print("75% Complete")
    return


def save_wav(file_name):
    wav_file=wave.open(file_name,"w")

    global audio
    global msam
    
    nchannels = 1

    sampwidth = 2

    nframes = len(audio)
    comptype = "NONE"
    compname = "not compressed"
    wav_file.setparams((nchannels, sampwidth, sampleRate, nframes, comptype, compname))
    
    for sample in audio:
        wav_file.writeframes(struct.pack('h', int( sample/(abs(msam)/.95) * 32767.0 )))

    wav_file.close()

    return

print("Generating Waveform")
generate_wave()

save_wav(saveFile)
print("Completed without error")
print("Saved to",saveFile)
times = np.linspace(0, 2696/sampleRate, 2696)
plt.figure(figsize=(12,6))
plt.plot(times, audio)
plt.title('Waveform')
plt.ylabel('Amplitude')
plt.xlabel('Time (s)')
plt.xlim(0, len(audio)/sampleRate)
plt.show()
