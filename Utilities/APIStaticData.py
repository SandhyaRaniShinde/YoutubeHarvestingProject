import os

class EnvironmentReader:
    def __init__(self):
        pass

    def get_specific_variable(self, variable_name):
        return os.environ.get(variable_name)
