import yaml

def get_schema():
    with open('schema.yaml', 'r') as f:
        return yaml.safe_load(f.read())