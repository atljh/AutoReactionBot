import json
import os

CONFIG_FILE = "config.json"

def load_config():
    if not os.path.exists(CONFIG_FILE):
        raise FileNotFoundError(f"{CONFIG_FILE} does not exist.")
    with open(CONFIG_FILE, "r") as file:
        return json.load(file)

def save_config(config_data):
    with open(CONFIG_FILE, "w") as file:
        json.dump(config_data, file, indent=4)

def update_config(key, value):
    config = load_config()
    config[key] = value
    save_config(config)
