import subprocess
import logging
import os
from abc import ABCMeta, abstractmethod
from collections import namedtuple
import requests
from cassandra.cqlengine.management import sync_table
from cassandra.cqlengine.models import ModelMetaClass

logger = logging.getLogger(__name__)

class SimpleCQLSchema(object):
    def cassandra_schema(self):
        data = open(self.schema, "r").read().split(";")
        return filter(lambda y: len(y), map(lambda x: x.strip(), data))

AutoGenerateSolrResources = namedtuple("AutoGenerateSolrResources", ["table"])
ExplicitSolrSchema = namedtuple("ExplicitSolrSchema", ["table"])

class Installer(object):
    __metaclass__ = ABCMeta

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
        logger.info("Post init, nothing to do.")

    def _install(self):
        self.post_init()
        logger.info("post_init() complete")

        if self._cassandra_schema:
            self.install_cassandra_schema()
        if self._cassandra:
            self.install_cassandra()
        if self._search:
            self.install_search_schema()
        if self._graph:
            self.install_graph_schema()
            self.install_graph()

        # set up tutorials

        logger.info("Done with install.")

    def install_cassandra_schema(self):
        # do not override
        logger.info("Applying schema {}".format(self.schema))

        self.context.session.set_keyspace(self.keyspace)
        for table in self.cassandra_schema():
            if isinstance(table, ModelMetaClass):
                sync_table(table)
            else:
                self.context.session.execute(table)


    def install_graph_schema(self):
        from firehawk.ddl import ParsedCommand
        for statement in self.graph_schema():
            logging.info("Schema %s", statement)
            if isinstance(statement, ParsedCommand):
                statement = str(statement)
            self.context.session.execute_graph(statement)


    def install_search_schema(self):
        logging.info("Setting up search schema")
        tables = self.search_schema()
        keyspace = self.keyspace
        host = "localhost"
        for table in tables:
            if isinstance(table, AutoGenerateSolrResources):
                url = "http://{}:8983/solr/admin/cores?action=CREATE&name={}.{}&generateResources=true&reindex=true".format(host, keyspace, table.table)
                logging.info(url)
                logging.info(requests.get(url))


    @abstractmethod
    def cassandra_schema(self):
        raise NotImplementedError("Cassandra schema required.")

    # @abstractmethod
    def graph_schema(self):
        raise NotImplementedError("Graph schema required.")

    # @abstractmethod
    def search_schema(self):
        # should return a list of SearchSchema classes
        raise NotImplementedError("Search schema required.")

    @abstractmethod
    def install_cassandra(self):
        raise NotImplementedError("Cassandra data required")


    # @abstractmethod
    def install_graph(self):
        logger.info("Graph requested but not implemented")
        raise NotImplementedError()

    @property
    def schema(self):
        return os.path.join(self.context.root, "schema.cql")

    @property
    def keyspace(self):
        return self.context.session.keyspace

Installer.register(SimpleCQLSchema)
