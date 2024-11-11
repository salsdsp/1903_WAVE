import math
import wave
import struct
import matplotlib.pyplot as plt
import numpy as np

audio = []
sampleRate = 44100.0
saveFile = "Waveforms/cursed_two.wav"

def myWave(sample):
    lsam = 0
    for harm in range(1,2**16):
        lsam += math.sin(harm*sample + 270/harm**2)/harm**1.5
    return lsam

def generate_wave(volume=0.5):

    global audio

    for x in range(0,2696):
        sample = 2 * math.pi * 16.351 * ( x / sampleRate )
        audio.append(volume * myWave(sample))
    return


def save_wav(file_name):
    wav_file=wave.open(file_name,"w")

    nchannels = 1

    sampwidth = 2

    nframes = len(audio)
    comptype = "NONE"
    compname = "not compressed"
    wav_file.setparams((nchannels, sampwidth, sampleRate, nframes, comptype, compname))

    for sample in audio:
        wav_file.writeframes(struct.pack('h', int( sample * 32767.0 )))

    wav_file.close()

    return


generate_wave()

save_wav(saveFile)
print("Completed without error.")
print("Saved to",saveFile)
times = np.linspace(0, 2696/sampleRate, 2696)
plt.figure(figsize=(12,6))
plt.plot(times, audio)
plt.title('Waveform')
plt.ylabel('Amplitude')
plt.xlabel('Time (s)')
plt.xlim(0, len(audio)/sampleRate)
plt.show()
