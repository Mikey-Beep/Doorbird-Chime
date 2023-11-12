from pathlib import Path
import io
import threading
from flask import Flask, Response, send_file
from common.config.config import Config
from watcher import Watcher

app = Flask(__name__)
config_path = Path(__file__).parent.parent / 'conf' / 'conf.yml'
config = Config.from_yaml(config_path)
watcher = Watcher(config.doorbell_ip, config.user,
                  config.password, config.event_retention_count)


@app.route('/motion', methods=['GET'])
def motion():
    watcher_thread = threading.Thread(
        target=watcher.save_event_set, name='Watcher-Motion', args=('motion',))
    watcher_thread.start()
    return Response(status=200)


@app.route('/ring', methods=['GET'])
def ring():
    watcher_thread = threading.Thread(
        target=watcher.save_event_set, name='Watcher-Ring', args=('ring',))
    watcher_thread.start()
    return Response(status=200)


@app.route('/current_image', methods=['GET'])
def current():
    return send_file(io.BytesIO(watcher.images[-1]), mimetype='image/jpeg')


app.run(host='0.0.0.0', port=80)
