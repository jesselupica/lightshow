import sys
import spotipy
import spotipy.util as util
import json 
from time import sleep
scope = 'user-read-playback-state'

client_id='529584eb85b845aba71c95fb9824b037'
client_secret='a106571adcb34f76a07a5656cce326f4'
redirect_uri='http://localhost/'
username = 'jesselupica'

class SpotifyIntegration:
    def __init__(self):
        self.token = util.prompt_for_user_token(username, scope, client_id, client_secret, redirect_uri)
        self.is_chill = self.query_loop()
        self.detection_failure = self.is_chill is None

    def query_loop(self):
        if self.token:
            sp = spotipy.Spotify(auth=self.token)
            results = sp.current_playback(market='US')
            #print results
            song_id = results['item']['id']
            song_name = results['item']['name']
            is_chill = sp.audio_features([song_id])[0]['energy'] < 0.5
            return is_chill
        else:
            print "Can't get token for", username
            return None

    def run_loop(self):
        while True:
            is_chill = self.query_loop()
            self.detection_failure = is_chill is None
            self.is_chill = is_chill
            sleep(1)

if __name__ == '__main__':
    s = SpotifyIntegration()
    print s.is_chill