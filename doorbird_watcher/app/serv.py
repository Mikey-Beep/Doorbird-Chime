import json, base64
from pathlib import Path
from flask import Flask, request, Response
from config import Config

app = Flask(__name__)
config_path = Path(__file__).parent.parent / 'conf' / 'conf.yml'
config = Config.from_yaml(config_path)

@app.route('/motion', methods = ['GET'])
def motion():
    return Response(status = 200)

app.run(host = '0.0.0.0', port = 80)