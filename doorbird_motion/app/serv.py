from flask import Flask, request, Response

app = Flask(__name__)

@app.route('/motion')
def record_motion():
    return Response(status = 200)

app.run(host = '0.0.0.0', port = 80)