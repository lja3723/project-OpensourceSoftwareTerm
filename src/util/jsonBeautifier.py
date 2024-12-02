import json

def toString(jsonObj):
    return json.dumps(jsonObj, indent=4)


def print(jsonObj):
    print(json.dumps(jsonObj, indent=4))