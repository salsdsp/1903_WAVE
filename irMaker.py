import math
import wave
import struct
import matplotlib.pyplot as plt
import numpy as np
import random as rand

audio = []
sampleRate = 44100.0
irLength = 10
delay = 0.1
delay = int(sampleRate*delay)
irLength *= int(sampleRate)
lfoFreq = 440
saveFile = "GenIRs/test3.wav"
msam = 0.0

"""
def myWave(sample):
    n = 0
    for harm in range(1,2**12):
        n += math.cos(harm*sample)**(11-int(11 * math.cos(harm*sample)/harm**2))/harm**1.5
    return n
"""

def generate_wave(volume=0.5):

    global audio, msam

    for x in range(0, delay):
        if(x%rand.randint(137,217)==0):
            audio.append(rand.random()*.7*math.sin(x))
        else:
            audio.append(0)
    for x in range(0,irLength):
        lfo = 2 * math.pi * math.sin(x*lfoFreq) * ( x / sampleRate )
        #temp = volume * myWave(sample)
        temp = rand.random()*((irLength-x)/irLength)**5 * math.sin(lfo)
        if abs(temp) > abs(msam):
            msam = temp
        audio.append(temp)
        #audio[x-1] *= audio[x]
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
times = np.linspace(0, (delay+irLength)/sampleRate, (delay+irLength))
plt.figure(figsize=(15,6))
plt.plot(times, audio)
plt.title('Waveform')
plt.ylabel('Amplitude')
plt.xlabel('Time (s)')
plt.xlim(0, len(audio)/sampleRate)
plt.show()
