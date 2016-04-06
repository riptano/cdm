import logging
from gevent.pool import Pool
from progressbar import ProgressBar

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



    def load(self, table):
        cache = {}

        def save(row):
            (query, values) = self.get_insert(row, table)
            try:
                prepared = cache[query]
            except:
                prepared = self.session.prepare(query)
                cache[query] = prepared
            bound = prepared.bind(values)
            self.session.execute(bound)

        pool = Pool(100)
        i = 0
        print "Loading {}".format(table)
        with ProgressBar(max_value=len(self.dataframe)) as p:
            for _ in pool.imap_unordered(save, self.iter()):
                i += 1
                if i % 10 == 0:
                    p.update(i)






