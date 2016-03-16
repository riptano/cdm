import subprocess

class Installer(object):
    context = None

    _search = False
    _graph = False
    _cassandra = True


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

        if self._cassandra:
            self.install_cassandra()
        if self._search:
            self.install_search()
        if self._graph:
            self.install_graph()

        self.context.feedback("Done with install.")

    def install_schema(self):
        # do not override
        self.context.feedback("Applying schema {}".format(self.schema))

        host = self.context.session.hosts[0].address
        command = "cqlsh -k {} -f {} {}".format(self.keyspace, self.schema, host)
        subprocess.call(command, shell=True)


    def cassandra_schema(self):
        raise NotImplementedError("Cassandra schema required.")

    def graph_schema(self):
        raise NotImplementedError("Graph schema required.")

    def search_schema(self):
        raise NotImplementedError("Search schema required.")

    def install_cassandra(self):
        raise NotImplementedError("Cassandra data required")

    def install_search(self):
        self.context.feedback("Search requested but not implemented")
        raise NotImplementedError()

    def install_graph(self):
        self.context.feedback("Graph requested but not implemented")
        raise NotImplementedError()

    @property
    def schema(self):
        return self.context.root + "/schema.cql"

    @property
    def keyspace(self):
        return self.context.session.keyspace
