import subprocess

class Installer(object):
    context = None

    search = False
    graph = False


    def __init__(self, context):
        # do not override
        self.context = context

    def post_init(self):
        # will get called after init
        pass

    def install(self):
        self.install_schema()

        if self.search:
            self.install_search()
        if self.graph:
            self.install_graph()

    def install_schema(self):
        # do not override
        self.context.feedback("Applying schema {}".format(self.schema))
        command = "cqlsh -k {} -f {} ".format(self.keyspace, self.schema)
        subprocess.call(command, shell=True)

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
