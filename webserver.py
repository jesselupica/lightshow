import json
from globalvars import light_visualizer
from flask import Flask, request

app = Flask(__name__)

def run_server():
    app.run(host='0.0.0.0', port=5001)

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
    light_visualizer = lightshow.get_vis()
    if light_visualizer.mode == 'VISUALIZE_MUSIC':
        light_visualizer.set_color(light_visualizer.static_color)
    else:
        light_visualizer.turn_on_music_visualization()
    return "1"

@app.route('/api/setHue', methods=['POST'])
def set_hue():
    data = request.form.to_dict()
    print(float(data['hue']))
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

@app.route('/api/setSpectrum', methods=['POST'])
def set_spec():
    data = request.form.to_dict()
    if data['spectrum'] == 'FULL':
        light_visualizer.subspectrum = 0
    elif data['spectrum'] == 'REDS':
        light_visualizer.subspectrum = 1
    elif data['spectrum'] == 'GREENS':
        light_visualizer.subspectrum = 2
    elif data['spectrum'] == 'BLUES':
        light_visualizer.subspectrum = 3
    print(light_visualizer.subspectrum)
    return "1"

@app.route('/api/setStaticColor', methods=['POST'])
def set_static_color():  
    data = request.form.to_dict()
    light_visualizer.set_color(data['color'].upper()) 
    return "1"

@app.route('/api/state', methods=['GET'])
def get_state():
    try:
        return json.dumps(light_visualizer.get_state())
    except Exception as e:
        print "it didnt work"
        print e

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001)
    print "testing main"
