from flask import Flask, request, Response
from test_broadcast import TestBroadcaster
from config import ConfigManager

app = Flask(__name__)
config_manager = ConfigManager()

@app.route('/test_broadcast', methods = ['GET'])
def test_broadcast():
    broadcaster = TestBroadcaster()
    broadcaster.broadcast(config_manager.config['test_packet'])
    return Response(status = 200)

@app.route('/config', methods = ['POST'])
def write_config():
    config_manager.config['user'] = request.json['user']
    config_manager.config['password'] = request.json['password']
    config_manager.config['sound_file'] = request.json['sound_file']
    config_manager.config['sleep_start'] = request.json['sleep_start']
    config_manager.config['sleep_end'] = request.json['sleep_end']
    try:
        config_manager.config['test_packet'] = request.json['test_packet']
    except:
        pass
    config_manager.save_config()
    return Response(status = 200)

app.run(host = '0.0.0.0', port = 80)