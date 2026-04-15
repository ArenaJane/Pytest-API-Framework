import os
import yaml

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_DIR = os.path.join(BASE_DIR, 'config', 'config.yaml')

def config_load():
    with open(CONFIG_DIR, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

config = config_load()