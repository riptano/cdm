from collections import OrderedDict

class Importer(object):
    session = None
    dataframe = None
    transformation = None

    def __init__(self, session, dataframe, transformation=None):
        self.session = session
        self.dataframe = dataframe
        self.transformation = transformation

    def transform(self, row):
        if self.transformation:
            return self.transformation(row)
        return dict(row)

    def iter(self):
        tmp = self.dataframe.iterrows()
        for i, row in tmp:
            yield self.transform(row)

