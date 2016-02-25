import urllib2
from base64 import b64encode
import os.path

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


    def download(self, url):
        """
        returns a file pointer
        auto caches download

        :param url:
        :param cache:
        :return:
        """
        encoded = b64encode(url)
        cache = self.cache_dir + encoded

        if not os.path.exists(cache):
            with open(cache, 'w') as fp:
                data = urllib2.urlopen(url)
                fp.write(data.read())

        fp = open(cache, 'r')
        return fp





