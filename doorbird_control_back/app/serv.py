import json, base64
from pathlib import Path
from flask import Flask, request, Response
from test_broadcast import TestBroadcaster
from config import ConfigManager
from sounds import SoundManager

app = Flask(__name__)
config_manager = ConfigManager()
sound_manager = SoundManager()

@app.route('/test_broadcast', methods = ['GET'])
def test_broadcast():
    broadcaster = TestBroadcaster()
    broadcaster.broadcast(config_manager.config['test_packet'])
    return Response(status = 200)

@app.route('/config', methods = ['GET', 'POST'])
def write_config():
    if request.method == 'GET':
        temp_conf = config_manager.config
        temp_conf['test_packet'] = base64.b64encode(temp_conf['test_packet']).decode('ascii')
        return Response(status = 200, response = json.dumps(temp_conf))
    elif request.method == 'POST':
        config_manager.config['user'] = request.json['user']
        config_manager.config['password'] = request.json['password']
        config_manager.config['sound_file'] = request.json['sound_file']
        config_manager.config['sleep_start'] = request.json['sleep_start']
        config_manager.config['sleep_end'] = request.json['sleep_end']
        try:
            config_manager.config['test_packet'] = request.json['test_packet']
        except:
            pass
        config_manager.save_config()
        return Response(status = 200)

@app.route('/sound_files', methods = ['GET'])
def list_sound_files():
    return Response(status = 200, response = json.dumps(sound_manager.list_sounds()))

@app.route('/upload_sound', methods = ['POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return Response(status = 400)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            return Response(status = 400)
        if file:
            file.save(Path(__file__).parent.parent / 'sounds' / file.filename)
            return Response(status = 200)

app.run(host = '0.0.0.0', port = 80)