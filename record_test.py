from sys import byteorder
from array import array
from struct import pack
from scipy.io import wavfile
import time
import math
import numpy
import pyaudio
import wave

THRESHOLD = 500
CHUNK_SIZE = 1024
RECORD_SECONDS = 30
FORMAT = pyaudio.paInt16
RATE = 44100

def get_amplitude_at_frequency(freq, aud_data, samp_freq):
    #samp_freq, snd = wavfile.read('440_sine.wav')
    #s1 = snd[:,0]
    #s2 = snd[:,1]
    s1 = numpy.array(aud_data)
    n = len(s1) 
    p = numpy.fft.fft(s1) / float(n) # take the fourier transform 

    magnitude = [math.sqrt(x.real**2 + x.imag**2) for x in p]
    index = int(int(freq) * n / int(samp_freq))

    return magnitude[index]

def get_dominant_frequency(samp_freq, aud_data):
    #samp_freq, snd = wavfile.read('440_sine.wav')
    #s1 = snd[:,0]
    #s2 = snd[:,1]
    s1 = numpy.array(aud_data)
    n = len(s1) 
    p = numpy.fft.fft(s1) / float(n) # take the fourier transform 

    magnitude = [math.sqrt(x.real**2 + x.imag**2) for x in p]
    max_mag = -float('inf')
    max_index = -1
    for i, x in enumerate(magnitude):
        if x > max_mag:
            max_mag= x
            max_index = i

    return max_index * samp_freq / n

def record():
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=1, rate=RATE,
        input=True, output=True,
        frames_per_buffer=CHUNK_SIZE)

    r = array('h')
    start = time.time()
    print("Start recording...")

    for i in range(0, int(RATE / CHUNK_SIZE * RECORD_SECONDS)):
        # little endian, signed short
        snd_data = array('h', stream.read(CHUNK_SIZE))
        if byteorder == 'big':
            snd_data.byteswap()
        r.extend(snd_data)

        #if len(samp) > sample_count * len(snd_data):

        freq = get_dominant_frequency(RATE, snd_data)
        #print(snd_data[:50])
        print(freq)
        print(("440 mag", get_amplitude_at_frequency(440, snd_data, RATE)))
            #samp = array('h')
        #samp.extend(snd_data)

    print(time.time() - start)

    stream.stop_stream()
    stream.close()

    r_stream = p.open(format=p.get_format_from_width(width=2), channels=1, rate=RATE, output=True)
    r_stream.write(r.tobytes())
    r_stream.stop_stream()
    r_stream.close()

    p.terminate()
    

if __name__ == '__main__':
    print("please speak a word into the microphone")
    record()
    print("done - result written to demo.wav")
