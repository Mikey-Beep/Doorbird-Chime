import json, base64
from pathlib import Path
from flask import Flask, request, Response
from test_broadcast import TestBroadcaster
from config import Config
from sounds import SoundManager

app = Flask(__name__)
config_path = Path(__file__).parent.parent / 'conf' / 'conf.yml'
config = Config.from_yaml(config_path)
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
    broadcaster.broadcast(base64.b64decode(config.test_packet.encode('ascii')))
    return Response(status = 200)

@app.route('/config', methods = ['GET', 'POST'])
def write_config():
    if request.method == 'GET':
        return Response(status = 200, response = json.dumps(config.__dict__))
    elif request.method == 'POST':
        config.update(request.json)
        with config_path.open('w') as config_file:
            config_file.write(config.to_yaml())
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