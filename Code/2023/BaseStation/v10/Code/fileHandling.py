import yaml

def save2File(obj, filename):
    with open(filename, 'w') as f:
        yaml.dump(obj, f, default_flow_style=False)

def load4File(filename):
    with open(filename, 'r') as f:
        return yaml.load(f, Loader=yaml.FullLoader)