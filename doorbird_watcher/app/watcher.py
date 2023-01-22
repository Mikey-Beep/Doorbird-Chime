from config import Config
import requests, threading, time

class Watcher:
    def __init__(self, config: Config):
        self.config = config
        self.images = [self.get_current_image()]
        self.watcher_thread = threading.Thread(target = self.watch, name = 'Watcher')
        self.watcher_thread.start()

    def get_current_image(self):
            session = requests.Session()
            session.auth = (self.config.user, self.config.password)
            session.verify = False
            response = session.get(f'https://{self.config.doorbell_ip}/bha-api/image.cgi')
            print('Image retrieved from doorbell.')
            return response.content

    def watch(self):
        while True:
            time.sleep(5)
            self.images.append(self.get_current_image())
            self.images = self.images[-3:]