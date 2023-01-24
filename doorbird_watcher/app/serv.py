from pathlib import Path
from flask import Flask, request, Response
from config import Config
from watcher import Watcher
import threading

app = Flask(__name__)
config_path = Path(__file__).parent.parent / 'conf' / 'conf.yml'
config = Config.from_yaml(config_path)
watcher = Watcher(config)

@app.route('/motion', methods = ['GET'])
def motion():
    watcher_thread = threading.Thread(target = watcher.save_event_set, name = 'Watcher', args = ('motion',))
    watcher_thread.start()
    return Response(status = 200)

@app.route('/current', methods = ['GET'])
def current():
    return Response(status = 200, response = watcher.get_current_image(), mimetype = 'image/jpeg')

app.run(host = '0.0.0.0', port = 80)