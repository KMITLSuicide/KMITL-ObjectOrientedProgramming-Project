from typing import Dict

class Config:
    def __init__(self, config: Dict):
        self.config = config

    def __getitem__(self, key):
        return self.config[key]

    def __getattr__(self, key):
        return self.config[key]

config = {
    "app_name": "KMITL-ObjectOrientedProgramming-Project",
    "log_level": "debug",
    "api_host" : "127.0.0.1",
    "api_port" : 4000
    }

config = Config(config)