
class Context(object):
    session = None
    cache_dir = None
    dataset = None

    def __init__(self, dataset, session, cache_dir):
        self.dataset = dataset
        self.session = session
        self.cache_dir = cache_dir




