class Importer(object):
    session = None
    dataframe = None
    fields = None

    def __init__(self, session, dataframe, fields):
        self.session = session
        self.dataframe = dataframe
        self.fields = fields

    def map(self, f):
        pass
