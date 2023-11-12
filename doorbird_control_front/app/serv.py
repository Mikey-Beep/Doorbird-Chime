import json
import io
from flask import Flask, render_template, Response, request, send_file
import requests

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/motion', methods=['GET'])
def motion():
    return render_template('motion.html')


@app.route('/ring', methods=['GET'])
def ring():
    return render_template('ring.html')


@app.route('/logs', methods=['GET'])
def logs():
    return render_template('logs.html')


@app.route('/current', methods=['GET'])
def current():
    return render_template('current.html')


@app.route('/events/<event_type>', methods=['GET'])
def motion_events(event_type: str):
    url = f'http://control-back/events/{event_type}'
    response = requests.get(url, timeout=10)
    return Response(status=200, response=json.dumps(response.json()))


@app.route('/events/<event_type>/<event_timestamp>', methods=['GET'])
def motion_event(event_type: str, event_timestamp: str):
    url = f'http://control-back/events/{event_type}/{event_timestamp}'
    response = requests.get(url, timeout=10)
    return Response(status=200, response=json.dumps(response.json()))


@app.route('/send_test', methods=['GET'])
def send_test_packet():
    url = 'http://control-back/test_broadcast'
    requests.get(url, timeout=10)
    return render_template('index.html')


@app.route('/get_config', methods=['GET'])
def get_config():
    url = 'http://control-back/config'
    resp = requests.get(url, timeout=10)
    return Response(status=200, response=json.dumps(resp.json()))


@app.route('/send_config', methods=['POST'])
def send_config():
    url = 'http://control-back/config'
    requests.post(url, json=request.json, timeout=10)
    return Response(status=200)


@app.route('/send_sound', methods=['POST'])
def send_sound():
    url = 'http://control-back/sound_file'
    files = {k: (v.filename, v.stream, v.content_type, v.headers)
             for k, v in request.files.items()}
    requests.post(url, files, timeout=10)
    return Response(status=200)


@app.route('/get_sounds', methods=['GET'])
def get_sounds():
    url = 'http://control-back/sound_files'
    resp = requests.get(url, timeout=10)
    return Response(status=200, response=json.dumps(resp.json()))


@app.route('/image/<event_type>/<event_timestamp>/<image_name>', methods=['GET'])
def get_image(event_type: str, event_timestamp: str, image_name: str):
    url = f'http://control-back/image/{event_type}/{event_timestamp}/{image_name}'
    resp = requests.get(url, timeout=10)
    return send_file(io.BytesIO(resp.content), mimetype='image/jpeg')


@app.route('/get_logs', methods=['GET'])
def get_logs():
    url = 'http://control-back/log'
    resp = requests.get(url, timeout=10)
    return Response(status=200, response=json.dumps(resp.json()))


@app.route('/current_image', methods=['GET'])
def get_current_image():
    url = 'http://control-back/current_image'
    resp = requests.get(url, timeout=10)
    return send_file(io.BytesIO(resp.content), mimetype='image/jpeg')


@app.route('/trigger_ir', methods=['GET'])
def trigger_ir():
    requests.get('http://control-back/triger_ir', timeout=10)
    return Response(status=200)


app.run(host='0.0.0.0', port=80)
