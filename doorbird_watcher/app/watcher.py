from config import Config
from pathlib import Path
from datetime import datetime
import requests, threading, time
from requests.auth import HTTPDigestAuth

class Watcher:
    def __init__(self, config: Config):
        self.config = config
        self.images = [self.get_current_image()]
        self.watcher_thread = threading.Thread(target = self.watch, name = 'Watcher')
        self.watcher_thread.start()

    def get_current_image(self):
            response = requests.get(f'https://{self.config.doorbell_ip}/bha-api/image.cgi', auth = HTTPDigestAuth(self.config.user, self.config.password), verify = False)
            print('Image retrieved from doorbell.')
            return response.content

    def watch(self):
        while True:
            time.sleep(5)
            self.images.append(self.get_current_image())
            self.images = self.images[-3:]
    
    def save_event_set(self, event_name: str):
        # Grab the most recent 3 images from the watcher.
        images = self.images.copy()
        # Grab two more images.
        time.sleep(5)
        images.append(self.get_current_image())
        time.sleep(5)
        images.append(self.get_current_image())
        # Build a directory to store the files for this event.
        image_dir = Path(__file__).parent.parent / 'images' / event_name / str(datetime.utcnow())
        image_dir.mkdir(parents = True, exist_ok = True)
        # Save the images into this directory.
        for i in range(len(images)):
            image_path = image_dir / f'{i}.jpg'
            with image_path.open('wb') as image_file:
                image_file.write(images[i])