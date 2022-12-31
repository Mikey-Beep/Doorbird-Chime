import json, base64
from pathlib import Path
from flask import Flask, request, Response
from test_broadcast import TestBroadcaster
from config import ConfigManager
from sounds import SoundManager

app = Flask(__name__)
config_manager = ConfigManager()
sound_manager = SoundManager()

@app.route('/api/docs', methods = ['GET'])
def serv_api():
    api_path: Path = Path(__file__).parent.parent / 'openapi' / 'openapi.yaml'
    with api_path.open() as api_file:
        file_content = api_file.read()
    return Response(status = 200, response = file_content)

@app.route('/test_broadcast', methods = ['GET'])
def test_broadcast():
    broadcaster = TestBroadcaster()
    broadcaster.broadcast(base64.b64decode(config_manager.config['test_packet'].encode('ascii')))
    return Response(status = 200)

@app.route('/config', methods = ['GET', 'POST'])
def write_config():
    if request.method == 'GET':
        return Response(status = 200, response = json.dumps(config_manager.config))
    elif request.method == 'POST':
        config_manager.config['user'] = request.json['user']
        config_manager.config['password'] = request.json['password']
        config_manager.config['sound_file'] = request.json['sound_file']
        config_manager.config['sleep_start'] = request.json['sleep_start']
        config_manager.config['sleep_end'] = request.json['sleep_end']
        try:
            config_manager.config['test_packet'] = request.json['test_packet']
        except Exception as e:
            print(e)
            pass
        config_manager.config['log_rotation_length'] = request.json['log_rotation_length']
        config_manager.save_config()
        return Response(status = 200)

@app.route('/sound_files', methods = ['GET'])
def list_sound_files():
    return Response(status = 200, response = json.dumps(sound_manager.list_sounds()))

@app.route('/sound_file', methods = ['POST'])
def sound_file():
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

@app.route('/log', methods = ['GET'])
def get_log():
    log_path = Path(__file__).parent.parent / 'log' / 'log.txt'
    log_data = []
    with log_path.open() as log_file:
        for line in log_file:
            line = line.strip().split('\u16bc')
            log_item = {
                'user': line[0],
                'event': line[1],
                'timestamp': line[2]
            }
            log_data.append(log_item)
    return Response(status = 200, response = json.dumps(log_data))

app.run(host = '0.0.0.0', port = 80)