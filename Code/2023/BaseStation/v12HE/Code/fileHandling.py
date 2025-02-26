import yaml
import consts
import json

def save2File(obj, filename):
    with open(filename, 'w') as f:
        yaml.dump(obj, f, default_flow_style=False)

def load4File(filename):
    with open(filename, 'r') as f:
        return yaml.load(f, Loader=yaml.FullLoader)

def save2FileJSON(obj, filename):
    with open(filename, "w") as outfile:
        json.dump(obj, outfile, indent=2)

def load4FileJSON(filename):
    with open(filename, 'r') as f:
        return json.load(f)

def get_paths(d):
    if isinstance(d, dict):
        for key, value in d.items():
            if type(value) != dict:
                yield f'{key}'
            yield from (f'{key}-{p}' for p in get_paths(value))
        
def getPointer(paths):
    result = consts.mapConfigJson
    for key in paths:
        result = result.get(key)
    return result