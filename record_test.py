from sys import byteorder
from array import array
from struct import pack
import time

import pyaudio
import wave

THRESHOLD = 500
CHUNK_SIZE = 1024
RECORD_SECONDS = 5
FORMAT = pyaudio.paInt16
RATE = 44100

def record():
    """
    Record a word or words from the microphone and 
    return the data as an array of signed shorts.

    Normalizes the audio, trims silence from the 
    start and end, and pads with 0.5 seconds of 
    blank sound to make sure VLC et al can play 
    it without getting chopped off.
    """
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=1, rate=RATE,
        input=True, output=True,
        frames_per_buffer=CHUNK_SIZE)

    r = array('h')
    start = time.time()
    print("Start recording...")
    count = 0
    for i in range(0, int(RATE / CHUNK_SIZE * RECORD_SECONDS)):
        count = i
        # little endian, signed short
        snd_data = array('h', stream.read(CHUNK_SIZE))
        if byteorder == 'big':
            snd_data.byteswap()
        r.extend(snd_data)
    print(time.time() - start, count)

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
