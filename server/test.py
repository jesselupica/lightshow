from gevent.pywsgi import WSGIServer
from flask import Flask

app = Flask(__name__)
app.debug = True

@app.route('/')
def index():
    return "Hello World!"
  
if __name__ == "__main__":

    http_server = WSGIServer(('0.0.0.0', 5000), app, certfile='/etc/letsencrypt/live/jesselupica.com/fullchain.pem', keyfile='/etc/letsencrypt/live/jesselupica.com/privkey.pem')
    http_server.serve_forever()
        
