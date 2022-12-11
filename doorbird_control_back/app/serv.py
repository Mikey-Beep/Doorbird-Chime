from flask import Flask
from test_broadcast import TestBroadcaster

app = Flask(__name__)

@app.route('/test_broadcast')
def test_broadcast():
    broadcaster = TestBroadcaster()
    broadcaster.broadcast()

app.run(host='0.0.0.0')