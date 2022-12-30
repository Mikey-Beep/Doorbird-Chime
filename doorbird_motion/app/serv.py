from pathlib import Path
from flask import Flask, request, Response
from config import Config
from datetime import datetime
import requests

config_path = Path(__file__).parent.parent / 'conf' / 'conf.yml'
image_directory_path = Path(__file__).parent.parent / 'images'

app = Flask(__name__)

@app.route('/motion')
def record_motion():
    config = Config(config_path)
    session = requests.Session()
    session.auth = (config.user, config.password)
    response = session.get(f'http://{config.doorbell_address}/bha-api/image.cgi')
    print(response.content)
    image_path = image_directory_path / f'{datetime.utcnow()}.jpg'
    with image_path.open('wb') as image_file:
        image_file.write(response.content)
    return Response(status = 200)

app.run(host = '0.0.0.0', port = 80)