import io
import json
import struct
import wave
import math
from pathlib import Path
import requests
from flask import Flask, request, Response, send_file
from test_broadcast import TestBroadcaster
from common.config.config import Config
from sounds import SoundManager
from requests.auth import HTTPDigestAuth

app = Flask(__name__)
config_path = Path(__file__).parent.parent / 'conf' / 'conf.yml'
conf = Config.from_yaml(config_path)
sound_manager = SoundManager()
image_dir = Path(__file__).parent.parent / 'images'
sound_dir = Path(__file__).parent.parent / 'sounds'


@app.route('/api/docs', methods=['GET'])
def serv_api():
    api_path: Path = Path(__file__).parent.parent / 'openapi' / 'openapi.yaml'
    with api_path.open() as api_file:
        file_content = api_file.read()
    return Response(status=200, response=file_content)


@app.route('/test_broadcast', methods=['GET'])
def test_broadcast():
    broadcaster = TestBroadcaster()
    broadcaster.broadcast(conf.test_message)
    return Response(status=200)


@app.route('/config', methods=['GET', 'POST'])
def config():
    if request.method == 'POST':
        conf.update(request.json)
        with config_path.open('w') as config_file:
            config_file.write(conf.to_yaml())
        gen_beep_file(conf.ping_freq, conf.ping_vol, conf.ping_dur)
        return Response(status=200)
    return Response(status=200, response=json.dumps(conf.to_dict()))


@app.route('/sound_files', methods=['GET'])
def list_sound_files():
    return Response(status=200, response=json.dumps(sound_manager.list_sounds()))


@app.route('/sound_file', methods=['POST'])
def sound_file():
    # check if the post request has the file part
    if 'file' not in request.files:
        return Response(status=400)
    file = request.files['file']
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == '':
        return Response(status=400)
    if file:
        file.save(sound_dir / file.filename)
        return Response(status=200)
    return Response(status=400)


@app.route('/log', methods=['GET'])
def get_log():
    log_path = Path(__file__).parent.parent / 'log' / 'log.txt'
    log_data = []
    with log_path.open() as log_file:
        for line in log_file:
            line = line.strip().split('\u16bc')
            while len(line) < 4:
                line.append('')
            log_item = {
                'user': line[0],
                'event': line[1],
                'timestamp': line[2],
                'message': line[3]
            }
            log_data.append(log_item)
    log_data = log_data[::-1]
    return Response(status=200, response=json.dumps(log_data))


@app.route('/events/<event_type>', methods=['GET'])
def get_motion_events(event_type: str):
    motion_path = image_dir / event_type
    try:
        events = sorted(
            [item.name for item in motion_path.iterdir()], reverse=True)
    except FileNotFoundError:
        events = []
    return Response(status=200, response=json.dumps(events))


@app.route('/events/<event_type>/<event_timestamp>', methods=['GET'])
def get_motion_event(event_type: str, event_timestamp: str):
    motion_path = image_dir / event_type
    try:
        events = [item.name for item in motion_path.iterdir()]
    except FileNotFoundError:
        events = []
    if event_timestamp not in events:
        return Response(status=404)
    image_paths = list((motion_path / event_timestamp).iterdir())
    images = sorted([{'event': event_timestamp, 'image': item.name}
                    for item in image_paths], key=lambda x: x['image'])
    return Response(status=200, response=json.dumps({'images': images}))


@app.route('/image/<event_type>/<event_timestamp>/<image_name>', methods=['GET'])
def get_image(event_type: str, event_timestamp: str, image_name: str):
    image_path = image_dir / event_type / event_timestamp / image_name
    return send_file(image_path, mimetype='image/jpeg')


@app.route('/current_image', methods=['GET'])
def get_current_image():
    url = 'http://watcher/current_image'
    resp = requests.get(url, timeout=10)
    return send_file(io.BytesIO(resp.content), mimetype='image/jpeg')


@app.route('/trigger_ir', methods=['GET'])
def trigger_ir():
    url = f'http://{conf.doorbell_ip}/bha-api/light-on.cgi'
    auth = HTTPDigestAuth(conf.user, conf.password)
    requests.get(url, auth=auth, verify=False, timeout=10)
    return Response(status=200)


def gen_beep_file(freq: int, vol: int, dur: int) -> Path:
    beep_path = sound_dir / 'beep.wav'
    wave_points = generate_wave(freq, vol, dur)
    print('Generating beep file.')
    beep_file = wave.open(str(beep_path), 'w')
    beep_file.setparams(
        (1, 2, 44100, len(wave_points), 'NONE', 'notcompressed'))
    for sample in wave_points:
        beep_file.writeframes(struct.pack('h', int(sample * 32767)))
    beep_file.close()


def generate_wave(freq: int, vol: int, dur: int) -> list[float]:
    print('Generating beep wave.')
    num_samples = dur * (44100 / 1000.0)
    return [(vol / 100) * math.sin(2 * math.pi * freq * (x / 44100)) for x in range(int(num_samples))]


app.run(host='0.0.0.0', port=80)
