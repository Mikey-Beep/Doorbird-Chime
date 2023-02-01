from pathlib import Path
from datetime import datetime
import requests, threading, time, shutil, urllib3
from requests.auth import HTTPDigestAuth

urllib3.disable_warnings()

class Watcher:
    def __init__(self, doorbell_ip: str, user: str, password: str, event_retention_count: int, image_spacing: int = 5):
        self.doorbell_ip = doorbell_ip
        self.user = user
        self.password = password
        self.event_retention_count = event_retention_count
        self.image_spacing = image_spacing
        self.images = [self.get_current_image()]
        self.watcher_thread = threading.Thread(target = self.watch, name = 'Watcher')
        self.watcher_thread.start()

    def get_current_image(self) -> bytes:
            response = requests.get(f'https://{self.doorbell_ip}/bha-api/image.cgi', auth = HTTPDigestAuth(self.user, self.password), verify = False)
            return response.content

    def watch(self) -> None:
        while True:
            time.sleep(self.image_spacing)
            self.images.append(self.get_current_image())
            self.images = self.images[-3:]
    
    def drop_old_images(self, event_name: str) -> None:
        event_dir = Path(__file__).parent.parent / 'images' / event_name
        events = sorted([event for event in event_dir.iterdir()], key = lambda x: x.name)
        if len(events) > self.event_retention_count:
            for i in range(len(events) - self.event_retention_count):
                shutil.rmtree(events[i])

    def save_event_set(self, event_name: str) -> None:
        # Grab the most recent 3 images from the watcher.
        images = self.images.copy()
        print('Storing images.')
        # Grab two more images.
        time.sleep(self.image_spacing)
        images.append(self.get_current_image())
        time.sleep(self.image_spacing)
        images.append(self.get_current_image())
        # Build a directory to store the files for this event.
        image_dir = Path(__file__).parent.parent / 'images' / event_name / str(datetime.utcnow())
        image_dir.mkdir(parents = True, exist_ok = True)
        # Save the images into this directory.
        for i in range(len(images)):
            image_path = image_dir / f'{i}.jpg'
            with image_path.open('wb') as image_file:
                image_file.write(images[i])
        print(f'Images stored in {image_dir}.')
        # Now check that we don't have too many events retained.
        self.drop_old_images(event_name)