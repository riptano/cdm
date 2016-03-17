import subprocess
import logging

from cassandra.cqlengine.management import sync_table
from cassandra.cqlengine.models import ModelMetaClass

class Installer(object):
    context = None

    _search = False
    _graph = False
    _cassandra = True
    _cassandra_schema = True


    def __init__(self, context):
        # do not override
        self.context = context

    def post_init(self):
        # will get called after init
        self.context.feedback("Post init, nothing to do.")

    def _install(self):
        self.install_schema()
        self.post_init()
        self.context.feedback("post_init() complete")

        if self._cassandra_schema:
            self.install_schema()
        if self._cassandra:
            self.install_cassandra()
        if self._search:
            self.install_search()
        if self._graph:
            self.install_graph()

        self.context.feedback("Done with install.")

    def install_schema(self):
        # do not override
        logging.info("Applying schema {}".format(self.schema))

        self.context.session.set_keyspace(self.keyspace)
        for table in self.cassandra_schema():
            if isinstance(table, ModelMetaClass):
                sync_table(table)
            else:
                self.context.session.execute(table)

        # host = self.context.session.hosts[0].address
        # command = "cqlsh -k {} -f {} {}".format(self.keyspace, self.schema, host)
        # subprocess.call(command, shell=True)


    def cassandra_schema(self):
        raise NotImplementedError("Cassandra schema required.")

    def graph_schema(self):
        raise NotImplementedError("Graph schema required.")

    def search_schema(self):
        # should return a dictionary of table
        raise NotImplementedError("Search schema required.")

    def install_cassandra(self):
        raise NotImplementedError("Cassandra data required")

    def install_search(self):
        logging.info("Search requested but not implemented")
        raise NotImplementedError()

    def install_graph(self):
        logging.info("Graph requested but not implemented")
        raise NotImplementedError()

    @property
    def schema(self):
        return self.context.root + "/schema.cql"

    @property
    def keyspace(self):
        return self.context.session.keyspace
