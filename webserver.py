from flask import Flask
app = Flask(__name__)


def start_server():
    app.run(host='0.0.0.0', port=5001)
    hello_world()

@app.route('/')
def hello_world():
    return 'Hello, World!'
