from sys import byteorder
from array import array
import pyaudio
import wave

class Recording:

    CHUNK_SIZE = 1024
    FORMAT = pyaudio.paInt16
    RATE = 44100

    def __init__(self, playback=True, file_name=None):
        p = pyaudio.PyAudio()
        self.playback = playback
        self.file_name = file_name
        if file_name:
            self.stream = wave.open(file_name, 'rb')
        else:
            self.stream = p.open(format=Recording.FORMAT, channels=1, rate=Recording.RATE,
                                input=True, output=True,
                                frames_per_buffer=Recording.CHUNK_SIZE)
        if playback:
            self.r_stream = self.stream 
        self.is_over = False

    def get_chunk(self):
        try:
            if self.file_name:
                sound_data = array('h', self.stream.readframes(Recording.CHUNK_SIZE))
            else: 
                sound_data = array('h', self.stream.read(Recording.CHUNK_SIZE))
                if byteorder == 'big':
                    sound_data.byteswap()
            if self.playback: 
                self.r_stream.write(sound_data.tobytes())
            return sound_data
        except:
            self.is_over = True
            return None

    def still_playing(self):
        return not self.is_over

    def spec(self):
        return Recording.CHUNK_SIZE, Recording.RATE 
