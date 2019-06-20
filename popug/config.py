import json
import os


def load():
    env = os.environ["POPUG_ENVIRONMENT"]
    with open(os.getcwd() + "/config.json") as config_file:
        return _update_paths(json.load(config_file)[env])


def _update_paths(json):
    json["friendsDir"] = os.getcwd() + json["friendsDir"]
    json["font"]["file"] = os.getcwd() + json["font"]["file"]
    return json
