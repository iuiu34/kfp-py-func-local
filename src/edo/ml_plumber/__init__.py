"""Main Package."""
import yaml


class Constants:
    def __init__(self):
        with open('vars.yaml', 'r') as f:
            variables = yaml.full_load(f)

        name = variables['name']
        project = variables['project']
        hostname = variables['hostname']
        version = variables['version']

        self.DEFAULT_IMAGE = f"{hostname}/{project}/{name}:v{version}"
        self.OUTPUT_PATH = f'gs://{name}'
        self.GCP_PROJECT = project
