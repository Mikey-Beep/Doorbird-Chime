#!/usr/bin/env python3
from flask import Flask, render_template
import requests

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

app.run(host='0.0.0.0', port = 80)
