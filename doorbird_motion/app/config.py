import yaml
from pathlib import Path

class Config:
    def __init__(self, conf_path: Path):
        # Open the config file and read it safely as yaml.
        with conf_path.open() as conf_file:
            config = yaml.safe_load(conf_file)
        # Pull config settings from the yaml.
        self.password = config['password']
        self.user = config['user']
        self.doorbell_address = config['doorbell_address']