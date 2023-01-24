import yaml
from pathlib import Path

class Config:
    def __init__(self):
        self.password = ''
        self.user = ''
        self.sound_file = ''
        self.sleep_start = ''
        self.sleep_end = ''
        self.test_packet = ''
        self.log_rotation_length = 100
        self.doorbell_ip = ''

    @classmethod
    def from_yaml(cls, conf_path: Path):
        with conf_path.open() as conf_file:
            config = yaml.safe_load(conf_file)
        new_config = Config()
        new_config.password = config['password']
        new_config.user = config['user']
        new_config.sound_file = config['sound_file']
        new_config.sleep_start =  config['sleep_start']
        new_config.sleep_end = config['sleep_end']
        new_config.test_packet = config['test_packet']
        new_config.log_rotation_length = config['log_rotation_length']
        new_config.doorbell_ip = config['doorbell_ip']
        return new_config
    
    def to_yaml(self):
        output = {}
        output['password'] = self.password
        output['user'] = self.user
        output['sound_file'] = self.sound_file
        output['sleep_start'] = self.sleep_start
        output['sleep_end'] = self.sleep_end
        output['test_packet'] = self.test_packet
        output['log_rotation_length'] = self.log_rotation_length
        output['doorbell_ip'] = self.doorbell_ip
        return yaml.dump(output)
    
    def update(self, json: dict):
        for k, v in json.items():
            if k in self.__dict__:
                self.__dict__[k] = v