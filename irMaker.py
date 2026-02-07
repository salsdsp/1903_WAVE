import math
import wave
import struct
import matplotlib.pyplot as plt
import numpy as np
import random as rand

audio = []
sampleRate = 44100.0
irLength = 10
delay = 0.2
delay = int(sampleRate*delay)
irLength *= int(sampleRate)
lfoFreq = 42
saveFile = "GenIRs/LP2.wav"
msam = 0.0
combJump = 1

"""
def myWav e(sample):
    n = 0
    for harm in range(1,2**12):
        n += math.cos(harm*sample)**(11-int(11 * math.cos(harm*sample)/harm**2))/harm**1.5
    return n
"""

def generate_wave(volume=0.5):

    global audio, msam

    for x in range(0, delay):
        if(x%rand.randint(7,17)==0):
            temp = rand.random()*.7*math.sin(x)
            audio.append(temp)
            if abs(temp) > abs(msam):
                msam = temp
        else:
            audio.append(0)
    for x in range(0, irLength*2):
        audio.append(0)
    for x in range(delay,irLength):
        lfo = 2 * math.pi * math.sin(x*lfoFreq*rand.random()) * ( x / sampleRate )
        #temp = volume * myWave(sample)
        temp = rand.random()*((irLength-x)/irLength)**6 * math.sin(lfo*rand.random())
        temp *= 3
        if abs(temp) > abs(msam):
            msam = temp
        audio[x] = temp
        """
    for x in range(0,irLength + delay):
        audio[x+combJump] = audio[x]*.5 + audio[x+combJump]*-0.5
        audio[x+combJump*2] = audio[x]*.5 + audio[x+combJump*2]*-0.5
        """
    for i in range(1,50):
        for x in range(combJump, irLength):
            audio[x-combJump] = audio[x] * 0.7 + audio[x-combJump]*0.3
    for i in range(1,12):
        for x in range(combJump, irLength):
            audio[x-combJump] = audio[x] * -0.7 + audio[x-combJump]*0.3
    msam = 0
    for x in range(0,irLength*2):
        if abs(audio[x] > abs(msam)):
            msam = audio[x]
    msam *= 0.95
    for x in range(0,irLength*2):
        audio[x] /= msam;
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
        wav_file.writeframes(struct.pack('h', int( sample * 32767.0 *0.95)))
        buffer.append(sample/(abs(msam)))
    audio = buffer

    wav_file.close()

    return

print("Generating Waveform")
generate_wave()

save_wav(saveFile)
print("Completed without error")
print("Saved to",saveFile)
times = np.linspace(0, (delay+irLength*2)/sampleRate, (delay+irLength*2))
plt.figure(figsize=(15,6))
plt.plot(times, audio)
plt.title('Waveform')
plt.ylabel('Amplitude')
plt.xlabel('Time (s)')
plt.xlim(0, len(audio)/sampleRate)
plt.show()
