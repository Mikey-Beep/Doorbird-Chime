from flask import Flask, Response, request
from pathlib import Path
# If this is a windows environment then import winsound, otherwise we'll use os to run a command.
try:
    import winsound
except:
    import os

app = Flask(__name__)

@app.route('/chime', methods = ['POST'])
def chime() -> Response:
    sound_file_path = Path(__file__).parent.parent / 'sounds' / request.json['sound_file']
    #Try and play a sound using winsound, if that fails try aplay for linux.
    try:
        print('Trying to play chime using winsound.')
        winsound.Play_sound(sound_file_path, winsound.SND_FILENAME)
    except:
        print(f'Winsound failed, trying aplay.')
        os.system(f'aplay -D plughw:1,0 {sound_file_path}')
    return Response(status = 200)

@app.route('/ping', methods = ['POST'])
def ping() -> Response:
    beep_file_path = Path(__file__).parent.parent / 'sounds' / 'beep.wav'
    try:
        print('Trying to beep using winsound.')
        winsound.Play_sound(beep_file_path, winsound.SND_FILENAME)
    except:
        print(f'Winsound failed, trying aplay.')
        os.system(f'aplay -D plughw:1,0 {beep_file_path}')
    return Response(status = 200)


app.run(host='0.0.0.0', port = 80)