import json
import os

config_file = os.path.join(os.getcwd(), 'config.json')

with open(config_file, 'r') as file:
    config_data = json.load(file)


def get_data(key):
    return config_data[key]


def set_data(key, value):
    config_data[key] = value

    with open(config_file, 'w') as file_json:
        json.dump(config_data, file_json, indent=3)
