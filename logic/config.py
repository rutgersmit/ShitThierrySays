import os
import json

def get_config(key:str) -> str:
    try:
        return os.environ[key.upper()]
    except KeyError:
        with open('config.json', 'r') as f:
            data = json.load(f)
            return data[key]