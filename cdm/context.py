import urllib2

class Context(object):
    session = None
    cache_dir = None
    dataset = None

    def __init__(self, dataset, session, cache_dir):
        self.dataset = dataset
        self.session = session
        # add trailing slash
        if not cache_dir.endswith("/"):
            cache_dir = cache_dir + "/"

        self.cache_dir = cache_dir


    def download(self, url, cache=True):
        """
        returns a file pointer

        :param url:
        :param cache:
        :return:
        """
        cache = self.cache_dir + ""



