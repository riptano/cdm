
class Context(object):
    session = None
    cache_dir = None

    def __init__(self, session, cache_dir=None):
        self.session = session
        self.cache_dir = cache_dir or self.get_default_cache_dir()

    def get_default_cache_dir(self):
        pass



