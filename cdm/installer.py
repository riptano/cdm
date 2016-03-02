
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
        pass

    def install_graph(self):
        pass




