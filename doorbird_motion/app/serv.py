from flask import Flask, request, Response
from config import Config

app = Flask(__name__)

@app.route('/motion')
def record_motion():
    config = Config()
    return Response(status = 200)

app.run(host = '0.0.0.0', port = 80)