import logging
from collections import OrderedDict
from gevent.pool import Pool

class Importer(object):
    session = None
    dataframe = None
    transformation = None

    def __init__(self, session, dataframe, transformation=None):
        """
        custom transformations accept a single row from a dataframe
        and should return a dictionary

        :param session:
        :param dataframe:
        :param transformation:
        :return:
        """
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

    def get_insert(self, row_as_dict, table):
        fields = row_as_dict.keys()
        field_list = ",".join(fields)
        placeholders = ",".join(["?"] * len(fields))
        statement = "INSERT INTO {} ({}) VALUES ({})".format(table, field_list, placeholders)
        return (statement, row_as_dict.values())
