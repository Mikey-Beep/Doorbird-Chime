#!/usr/bin/env python3
from flask import Flask, render_template, Response
import requests, json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_test')
def send_test_packet():
    url = 'http://back/test_broadcast'
    response = requests.request("GET", url, data='')
    print(response.text)
    return render_template('index.html')

@app.route('/get_config')
def get_config():
    url = 'http://back/config'
    resp = requests.request("GET", url, data='')
    return Response(status = 200, response = json.dumps(resp.json()))

@app.route('/get_sounds')
def get_sounds():
    url = 'http://back/sound_files'
    resp = requests.request("GET", url, data='')
    return Response(status = 200, response = json.dumps(resp.json()))

app.run(host='0.0.0.0', port = 80)
