from pathlib import Path
import yaml

class ConfigManager:
    def __init__(self):
        self.conf_path = Path(__file__).parent.parent / 'conf' / 'conf.yml'
        self.conf_path.parent.mkdir(parents = True, exist_ok = True)
        try:
            with self.conf_path.open() as conf_file:
                self.config = yaml.safe_load(conf_file)
        except FileNotFoundError:
            self.build_bare_config()
        
    def build_bare_config(self):
        config = {
            'password': '',
            'user': '',
            'sound_file': '',
            'sleep_start': '',
            'sleep_end': '',
            'test_packet': b''
        }
        self.config = config
        self.save_config()
        return config

    def save_config(self):
        with self.conf_path.open('w') as conf_file:
            conf_file.write(yaml.safe_dump(self.config))