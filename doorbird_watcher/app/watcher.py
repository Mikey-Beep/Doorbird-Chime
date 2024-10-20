"""This module interacts with the doorbell to retrieve images.
"""
from collections import deque
from pathlib import Path
from datetime import datetime
import threading
import time
import shutil
import requests
import urllib3
from requests.auth import HTTPDigestAuth

urllib3.disable_warnings()


class Watcher:
    """This Class authenticates with the doorbell and maintains a rolling 5 image history."""
    def __init__(self,
                 doorbell_ip: str,
                 user_credentials: tuple[str, str],
                 event_retention_count: int,
                 image_spacing: int = 5):
        self.doorbell_ip = doorbell_ip
        self.auth = HTTPDigestAuth(*user_credentials)
        self.event_retention_count = event_retention_count
        self.image_spacing = image_spacing
        self.image_dir = Path(__file__).parent.parent / 'images'
        self.images = deque(maxlen=5)
        self.images.append(self.get_current_image())
        self.watcher_thread = threading.Thread(
            target=self.watch, name='Watcher')
        self.watcher_thread.start()

    def get_current_image(self) -> bytes:
        """Get a current image from the doorbell.
        """
        url = f'https://{self.doorbell_ip}/bha-api/image.cgi'
        response = requests.get(url, auth=self.auth, verify=False, timeout=10)
        return response.content

    def watch(self) -> None:
        """Capture images for the rolling history.
        """
        while True:
            time.sleep(self.image_spacing)
            self.images.append(self.get_current_image())

    def drop_old_images(self, event_name: str) -> None:
        """Delete old saved images when new ones are captured.
        """
        event_dir = self.image_dir / event_name
        events = sorted(list(event_dir.iterdir()), key=lambda x: x.name)
        if len(events) > self.event_retention_count:
            for i in range(len(events) - self.event_retention_count):
                shutil.rmtree(events[i])

    def save_event_set(self, event_name: str) -> None:
        """Save a set of images when an event is triggered.
        """
        # Grab the most recent 3 images from the watcher.
        images = deque(list(self.images), maxlen=5)
        print('Storing images.')
        # Grab two more images.
        time.sleep(self.image_spacing)
        images.append(self.get_current_image())
        time.sleep(self.image_spacing)
        images.append(self.get_current_image())
        # Build a directory to store the files for this event.
        image_dir = self.image_dir / event_name / str(datetime.utcnow())
        image_dir.mkdir(parents=True, exist_ok=True)
        # Save the images into this directory.
        for i, image in enumerate(images):
            image_path = image_dir / f'{i}.jpg'
            with image_path.open('wb') as image_file:
                image_file.write(image)
        print(f'Images stored in {image_dir}.')
        # Now check that we don't have too many events retained.
        self.drop_old_images(event_name)
