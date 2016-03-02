
class Installer(object):
    context = None

    def __init__(self, context):
        # do not override
        self.context = context

    def post_init(self):
        # will get called after init
        pass

    def install_cassandra(self):
        raise NotImplementedError("Cassandra data required")

    def install_search(self):
        self.context.feedback("Search requested but not implemented")
        raise NotImplementedError()

    def install_graph(self):
        self.context.feedback("Graph requested but not implemented")
        raise NotImplementedError()




