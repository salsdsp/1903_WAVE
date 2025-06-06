import math
import wave
import struct
import matplotlib.pyplot as plt
import numpy as np
import random as rand

audio = []
sampleRate = 44100.0
saveFile = "Waveforms/combiwave_9.wav"
msam = 0.0

def myWave(sample):
    n = 0
    for harm in range(1,2**12):
        n += math.cos(harm*sample)**(12-int(11 * math.cos(harm*sample)/harm**2))/harm**1.5
    return n

def generate_wave(volume=0.5):

    global audio, msam

    for x in range(0,2696):
        sample = 2 * math.pi * 16.3516 * ( x / sampleRate )
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
    buffer = []
    
    nchannels = 1

    sampwidth = 2

    nframes = len(audio)
    comptype = "NONE"
    compname = "not compressed"
    wav_file.setparams((nchannels, sampwidth, sampleRate, nframes, comptype, compname))

    count = 0
    for sample in audio:
        wav_file.writeframes(struct.pack('h', int( sample/(abs(msam)/.95) * 32767.0 )))
        buffer.append(sample/(abs(msam)))
    audio = buffer

    wav_file.close()

    return

print("Generating Waveform")
generate_wave()

save_wav(saveFile)
print("Completed without error")
print("Saved to",saveFile)
times = np.linspace(0, 2696/sampleRate, 2696)
plt.figure(figsize=(15,6))
plt.plot(times, audio)
plt.title('Waveform')
plt.ylabel('Amplitude')
plt.xlabel('Time (s)')
plt.xlim(0, len(audio)/sampleRate)
plt.show()
