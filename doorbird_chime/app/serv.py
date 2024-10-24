"""This module is responsible for making sounds.
"""
from pathlib import Path
# If this is a windows environment then import winsound, otherwise we'll use os to run a command.
import os
try:
    import winsound
    SOUND_MODE = 'windows'
except ImportError:
    SOUND_MODE = 'linux'
from flask import Flask, Response, request

app = Flask(__name__)
sound_dir = Path(__file__).parent.parent / 'sounds'


@app.route('/chime', methods=['POST'])
def chime() -> Response:
    """This function handles playing a sound when the doorbell button is pressed.
    """
    sound_file_path = sound_dir / request.json['sound_file']
    if SOUND_MODE == 'windows':
        winsound.Play_sound(sound_file_path, winsound.SND_FILENAME)
    else:
        os.system(f'aplay -D plughw:1,0 {sound_file_path}')
    return Response(status=200)


@app.route('/ping', methods=['POST'])
def ping() -> Response:
    """This function handles playing a sound when motion is detected.
    """
    beep_file_path =  sound_dir / 'ping.wav'
    if SOUND_MODE == 'windows':
        winsound.Play_sound(beep_file_path, winsound.SND_FILENAME)
    else:
        os.system(f'aplay -D plughw:1,0 {beep_file_path}')
    return Response(status=200)


@app.route('/plex', methods=['POST'])
def plex_ping() -> Response:
    """This function handles playing a sound when plex has started.
    """
    beep_file_path =  sound_dir / 'plex.wav'
    if SOUND_MODE == 'windows':
        winsound.Play_sound(beep_file_path, winsound.SND_FILENAME)
    else:
        os.system(f'aplay -D plughw:1,0 {beep_file_path}')
    return Response(status=200)


app.run(host='0.0.0.0', port=80)
