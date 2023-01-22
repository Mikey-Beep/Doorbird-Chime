from pathlib import Path
from flask import Flask, request, Response
from config import Config
from watcher import Watcher
from datetime import datetime
import time

app = Flask(__name__)
config_path = Path(__file__).parent.parent / 'conf' / 'conf.yml'
config = Config.from_yaml(config_path)
watcher = Watcher(config)

@app.route('/motion', methods = ['GET'])
def motion():
    # Grab the most recent 3 images from the watcher.
    images = watcher.images.copy()
    # Grab two more images.
    time.sleep(5)
    images.append(watcher.get_current_image())
    time.sleep(5)
    images.append(watcher.get_current_image())
    # Build a directory to store the files for this motion event.
    motion_directory = Path(__file__).parent.parent / 'images' / 'motion' / str(datetime.utcnow())
    motion_directory.mkdir(parents = True, exist_ok = True)
    # Save the images into this directory.
    for i in range(len(images)):
        image_path = motion_directory / f'{i}.jpg'
        with image_path.open('wb') as image_file:
            image_file.write(images[i])
    return Response(status = 200)

app.run(host = '0.0.0.0', port = 80)