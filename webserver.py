import json
from HSVVisualizer import HSVVisualizer
from flask import Flask, request

app = Flask(__name__)
light_visualizer = HSVVisualizer(255, 255, 255)

@app.route("/")
def hello():
    return "Hello World!"

@app.route('/api/toggleLights', methods=['POST'])
def toggle_lights():  
    if light_visualizer.mode != 'OFF':
        light_visualizer.turn_off_lights()
    else: 
        light_visualizer.turn_on_music_visualization()
    return "1"

@app.route('/api/toggleFade', methods=['POST'])
def toggle_fade(): 
    if light_visualizer.mode == 'FADE':
        light_visualizer.turn_on_music_visualization()
    else:
        light_visualizer.turn_on_fade()
    return "1"

@app.route('/api/toggleVisMusic', methods=['POST'])
def toggle_music_vis():  
    if light_visualizer.mode == 'VISUALIZE_MUSIC':
        light_visualizer.set_color(light_visualizer.static_color)
    else:
        light_visualizer.turn_on_music_visualization()
    return "1"

@app.route('/api/setHue', methods=['POST'])
def set_hue():  
    data = request.form.to_dict()
    light_visualizer.set_hue(float(data['hue']))
    return "1"

@app.route('/api/setSat', methods=['POST'])
def set_sat(): 
    data = request.form.to_dict()
    light_visualizer.set_sat(float(data['sat']))
    return "1"
@app.route('/api/setBri', methods=['POST'])
def set_bri(): 
    data = request.form.to_dict()
    print(data)
    light_visualizer.set_brightness(float(data['bri']))
    return "1"

@app.route('/api/state', methods=['GET'])
def get_state():
    try:
        return json.dumps(light_visualizer.get_state())
    except Exception as e:
        print "it didnt work"
        print e

def run_server(visualizer):
    app.run(host='0.0.0.0', port=5001)
    light_visualizer = visualizer

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001)