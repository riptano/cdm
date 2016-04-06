from gevent.monkey import patch_all
import logging
import os.path
import imp
import inspect
from base64 import b64encode
import urllib2

from gevent.pool import Pool
import progressbar

import pandas
from cdm.installer import Installer
from cdm.importer import Importer

class InstallerNotFound(Exception): pass


class Context(object):
    root = None
    session = None
    cache_dir = None
    dataset = None
    keyspace = None

    @property
    def installer(self):
        post_install = os.path.join(self.root, "install.py")

        logging.info("Loading installer {}".format(post_install))
        module = imp.load_source("Installer", post_install)
        members = inspect.getmembers(module)

        matching = [c for (name, c) in members if isinstance(c, type)
                    and c is not Installer
                    and issubclass(c, Installer)]

        if not matching:
            raise InstallerNotFound()

        installer = matching[0](self)
        self.feedback("Installer found")
        return installer

    def __init__(self, root, dataset, session, cache_dir):
        self.root = root
        self.dataset = dataset
        self.session = session
        # add trailing slash
        if not cache_dir.endswith("/"):
            cache_dir = cache_dir + "/"

        self.cache_dir = cache_dir
        if not os.path.exists(self.cache_dir):
            raise Exception("Cache dir does not exist")


    def download(self, url):
        """
        downloads a single file to the cache
        returns a file pointer
        auto caches download

        :param url:
        :param cache:
        :return:
        """
        encoded = b64encode(url)
        cache = self.cache_dir + encoded

        logging.info("Downloading {}".format(url))
        if not os.path.exists(cache):
            with open(cache, 'w') as fp:
                data = urllib2.urlopen(url)
                fp.write(data.read())
            logging.info("Download finished")
        else:
            self.feedback("Found in cache, skipping")

        fp = open(cache, 'r')
        return fp

    def open_local(self, name):
        tmp = os.path.join(self.root, name)
        return open(tmp, "r")

    def clean_cache(self):
        """
        removes all data from this cache directory
        :return: None
        """
        for file in os.listdir(self.cache_dir):
            logging.info(os.remove(self.cache_dir + file))


    def feedback(self, msg):
        logging.info(msg)

    def save_dataframe_to_cassandra(self, dataframe, table,
                                    transformation=None):
        """
        :param session:
        :type session: cassandra.cluster.Session
        :param dataframe:
        :type dataframe: pandas.DataFrame
        :param table:
        :return:
        """
        logging.info("Saving dataframe to %s", table)
        importer = Importer(self.session, dataframe, transformation)
        importer.load(table)


    def prepare(self, table, fields):
        field_list = ",".join(fields)
        placeholders = ",".join(["?"] * len(fields))
        statement = "INSERT INTO {} ({}) VALUES ({})".format(table, field_list, placeholders)
        logging.info("preparing %s", statement)
        return self.session.prepare(statement)
