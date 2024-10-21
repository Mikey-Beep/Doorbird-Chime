"""This module handles providing the frontend for the doorbell controller.
"""
import json
import io
from flask import Flask, render_template, Response, request, send_file
import requests

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    """Serves the homepage.
    """
    return render_template('index.html')


@app.route('/motion', methods=['GET'])
def motion():
    """Serves the motion events page.
    """
    return render_template('motion.html')


@app.route('/ring', methods=['GET'])
def ring():
    """Serves the ring events page.
    """
    return render_template('ring.html')


@app.route('/logs', methods=['GET'])
def logs():
    """Serves the log page.
    """
    return render_template('logs.html')


@app.route('/current', methods=['GET'])
def current():
    """Serves the current image page.
    """
    return render_template('current.html')


@app.route('/events/<event_type>', methods=['GET'])
def motion_events(event_type: str):
    """Proxies the event list functionality.
    """
    url = f'http://control-back/events/{event_type}'
    response = requests.get(url, timeout=10)
    return Response(status=200, response=json.dumps(response.json()))


@app.route('/events/<event_type>/<event_timestamp>', methods=['GET'])
def motion_event(event_type: str, event_timestamp: str):
    """Proxies the event image list functionality.
    """
    url = f'http://control-back/events/{event_type}/{event_timestamp}'
    response = requests.get(url, timeout=10)
    return Response(status=200, response=json.dumps(response.json()))


@app.route('/send_test', methods=['GET'])
def send_test_packet():
    """Proxies the test broadcast functionality.
    """
    url = 'http://control-back/test_broadcast'
    resp = requests.get(url, timeout=10)
    return Response(status=resp.status_code)


@app.route('/test_ping', methods=['POST'])
def test_ping():
    """Proxies the tet ping functionality.
    """
    url = 'http://control-back/test_ping'
    resp = requests.post(url, timeout=10)
    return Response(status=resp.status_code)


@app.route('/get_config', methods=['GET'])
def get_config():
    """Proxies the get config functionality.
    """
    url = 'http://control-back/config'
    resp = requests.get(url, timeout=10)
    return Response(status=200, response=json.dumps(resp.json()))


@app.route('/send_config', methods=['POST'])
def send_config():
    """Proxies the update config functionality.
    """
    url = 'http://control-back/config'
    requests.post(url, json=request.json, timeout=10)
    return Response(status=200)


@app.route('/send_sound', methods=['POST'])
def send_sound():
    """Proxies the upload sound file functionality.
    """
    url = 'http://control-back/sound_file'
    files = {k: (v.filename, v.stream, v.content_type, v.headers)
             for k, v in request.files.items()}
    requests.post(url, files, timeout=10)
    return Response(status=200)


@app.route('/get_sounds', methods=['GET'])
def get_sounds():
    """Proxies the get sound list functionality.
    """
    url = 'http://control-back/sound_files'
    resp = requests.get(url, timeout=10)
    return Response(status=200, response=json.dumps(resp.json()))


@app.route('/image/<event_type>/<event_timestamp>/<image_name>', methods=['GET'])
def get_image(event_type: str, event_timestamp: str, image_name: str):
    """Proxies the get image functionality.
    """
    url = f'http://control-back/image/{event_type}/{event_timestamp}/{image_name}'
    resp = requests.get(url, timeout=10)
    return send_file(io.BytesIO(resp.content), mimetype='image/jpeg')


@app.route('/get_logs', methods=['GET'])
def get_logs():
    """Proxies the get log functionality.
    """
    url = 'http://control-back/log'
    resp = requests.get(url, timeout=10)
    return Response(status=200, response=json.dumps(resp.json()))


@app.route('/current_image', methods=['GET'])
def get_current_image():
    """Proxies the current image functionality.
    """
    url = 'http://control-back/current_image'
    resp = requests.get(url, timeout=10)
    return send_file(io.BytesIO(resp.content), mimetype='image/jpeg')


@app.route('/trigger_ir', methods=['GET'])
def trigger_ir():
    """Proxies the IR trigger functionality.
    """
    requests.get('http://control-back/triger_ir', timeout=10)
    return Response(status=200)


app.run(host='0.0.0.0', port=80)
