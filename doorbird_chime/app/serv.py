import math
import secrets
import struct
import wave
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
    try:
        freq = request.json['freq']
    except:
        freq = 400
    try:
        vol = request.json['vol']
    except:
        vol = 50
    try:
        dur = request.json['dur']
    except:
        dur = 500
    beep_file_path = gen_beep_file(freq, vol, dur)
    try:
        print('Trying to beep using winsound.')
        winsound.Play_sound(beep_file_path, winsound.SND_FILENAME)
    except:
        print(f'Winsound failed, trying aplay.')
        os.system(f'aplay -D plughw:1,0 {beep_file_path}')
    print('Removing beep file.')
    beep_file_path.unlink()
    return Response(status = 200)

def gen_beep_file(freq: int, vol: int, dur: int) -> Path:
    beep_path = Path(__file__).parent.parent / 'sounds' / secrets.token_hex()
    wave_points = generate_wave(freq, vol, dur)
    print('Generating beep file.')
    beep_file = wave.open(str(beep_path), 'w')
    try:
        beep_file.setparams((1, 2, 44100, len(wave_points), 'NONE', 'notcompressed'))
        for sample in wave_points:
            beep_file.writeframes(struct.pack('h', int(sample * 32767)))
        beep_file.close()
    except:
        beep_file.close()
        raise
    return beep_path

def generate_wave(freq: int, vol: int, dur: int) -> list[float]:
    print('Generating beep wave.')
    num_samples = dur * (44100 / 1000.0)
    return [(vol / 100) * math.sin(2 * math.pi * freq * (x / 44100)) for x in range(int(num_samples))]

app.run(host='0.0.0.0', port = 80)