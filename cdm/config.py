import yaml

class Config(object):
    data = None

    def __init__(self, fp):
        self.data = yaml.load(fp)
        pass

    def save(self, fp):
        pass


