import math
import wave
import struct

audio = []
sampleRate = 44100.0
saveFile = "output.wav"

def myWave(sample):
    lsam = 0
    for harm in range(1,2**16):
        lsam += math.sin(harm*sample)/harm
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
