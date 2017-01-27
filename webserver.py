from HSVVisualizer import HSVVisualizer
from flask import Flask

app = Flask(__name__)
light_visualizer = HSVVisualizer(255, 255, 255)

@app.route("/")
def hello():
    return "Hello World!"

@app.route('/api/toggleLights', methods=['POST'])
def toggleLights():  
    
    return "1"

@app.route('/api/toggleFade', methods=['POST'])
def tel_route():  
    return "1"

@app.route('/api/toggleVisMusic', methods=['POST'])
def tel_route():  
    return "1"

def run_server(visualizer):
    app.run(host='0.0.0.0', port=5001)
    light_visualizer = visualizer

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001)