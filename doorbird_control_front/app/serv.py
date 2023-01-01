#!/usr/bin/env python3
from flask import Flask, render_template, Response, request
import requests, json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_test')
def send_test_packet():
    url = 'http://control-back/test_broadcast'
    response = requests.request("GET", url, data='')
    print(response.text)
    return render_template('index.html')

@app.route('/get_config')
def get_config():
    url = 'http://control-back/config'
    resp = requests.request("GET", url, data='')
    return Response(status = 200, response = json.dumps(resp.json()))

@app.route('/send_config', methods = ['POST'])
def send_config():
    url = 'http://control-back/config'
    requests.request("POST", url, json=request.json)
    return Response(status = 200)

@app.route('/send_sound', methods = ['POST'])
def send_sound():
    requests.request(
        method='POST',
        url='http://control-back/sound_file',
        files={k: (v.filename, v.stream, v.content_type, v.headers) for k, v in request.files.items()}
    )
    return Response(status = 200)

@app.route('/get_sounds')
def get_sounds():
    url = 'http://control-back/sound_files'
    resp = requests.request("GET", url, data='')
    return Response(status = 200, response = json.dumps(resp.json()))

app.run(host='0.0.0.0', port = 80)
