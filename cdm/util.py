import os
import os.path
import subprocess
import urllib2

import yaml
from git import Repo
from importlib import import_module

from cassandra.cqlengine.connection import setup, get_session as get_db_session

# try to import the dse session
# if it works, monkey patch cqlengine to use dse session

from cdm.util import *
from cdm.context import Context
import imp
import inspect
from cdm.installer import Installer
import sys
from distutils.spawn import find_executable

DATASETS_URL = "https://raw.githubusercontent.com/cassandra-data-manager/cdm/master/datasets.yaml"

CDM_CACHE = os.getenv("CDM_CACHE", os.path.expanduser("~/.cdm/"))
CDM_PACKAGE_FILE = CDM_CACHE + "datasets.yaml"

class InstallerNotFound(Exception): pass

def list_datasets(search):
    print "Available datasets:"
    data = open_datasets()

    #TODO rank results
    found = 0
    for name, details in data.iteritems():
        if search and search not in name and search not in details['description']:
            continue

        found += 1
        print "{:20} {}".format(name, details['description'])

    if found == 0:
        print "No datasets found"


def open_datasets():
    with open(CDM_PACKAGE_FILE, 'r') as fp:
        data = yaml.load(fp)
    return data


def update_datasets():
    print "Updating datasets"
    fp = urllib2.urlopen(DATASETS_URL)
    data = fp.read()
    print data

    with open(CDM_PACKAGE_FILE, 'w') as d:
        d.write(data)

def normalize_dataset_name(dataset):
    return dataset.replace("-", "_")

def get_session(dataset, graph=False, host="localhost"):
    keyspace = normalize_dataset_name(dataset)
    if graph:
        try:
            from dse.cluster import Cluster
            from cassandra.cqlengine import connection
            connection.Cluster = Cluster
            print "Graph support enabled"
        except:
            pass

    session = connect(host=host, keyspace=keyspace)

    print "Creating keyspace"
    if keyspace not in session.cluster.metadata.keyspaces:
        cql = "create KEYSPACE {} WITH replication = {{'class': 'SimpleStrategy', 'replication_factor': 1}}".format(keyspace)
        session.execute(cql)

    if graph:
        graph_keyspace = keyspace + "_graph"


        try:
            session.execute_graph("system.dropGraph('{}')".format(graph_keyspace))
        except:
            pass

        session.execute_graph("system.createGraph('{}').build()".format(graph_keyspace))
        session.default_graph_options.graph_name = graph_keyspace
        print "Created graph keyspace {}".format(graph_keyspace)


    session.set_keyspace(keyspace)
    return session

def install(dataset,
            version="master",
            install_cassandra=True,
            install_graph=False,
            install_search=False,
            host=None):

    # check for cqlsh
    if not find_executable("cqlsh"):
        print "cqlsh could not be found.  Please add to your path."
        sys.exit(1)

    if install_graph:
        try:
            import dse
        except:
            print "--graph supplied but python dse module not installed."
            sys.exit(1)

    # check for dse module

    if dataset == ".":
        path = "."
        dataset = "test"
        cache_dir = ".cdmcache"
    else:
        y = open_datasets()
        repo = download_dataset(dataset, y[dataset]['url'])

        # returns the git repo
        # we should be on master now
        # do I need a specific version?
        repo.git.checkout(version)
        path = local_dataset_path(dataset)
        # this should be keyspace
        cache_dir = CDM_CACHE + dataset + "_cache"
        sys.path.append(path) # so imports work

    print "Connecting"

    session = get_session(dataset, install_graph, host=host)
    # load the schema

    if not os.path.exists(cache_dir):
        os.mkdir(cache_dir)

    context = Context(root=path,
                      dataset=dataset,
                      session=session,
                      cache_dir=cache_dir)

    # TODO move to tested function
    post_install = path + "/install.py"
    context.feedback("Loading installer {}".format(post_install))
    module = imp.load_source("Installer", post_install)
    members = inspect.getmembers(module)

    matching = [c for (name, c) in members if isinstance(c, type)
                                            and c is not Installer
                                            and issubclass(c, Installer)]
    if not matching:
        raise InstallerNotFound()


    installer = matching[0](context)
    installer._cassandra = install_cassandra
    installer._search = install_search
    installer._graph = install_graph
    installer._install()

def install_local(path, install_search, install_graph):
    pass


def local_dataset_path(dataset_name):
    return CDM_CACHE + dataset_name


def show_dataset_details(dataset_name):
    print "{}".format(dataset_name)

def download_dataset(dataset_name, dataset_url):
    local_git = local_dataset_path(dataset_name)
    if not os.path.exists(local_git):
        repo = Repo.clone_from(dataset_url, local_git)
        print "Downloaded"
    else:
        print "Repo exists, pulling latest"
        repo = Repo(local_git)
        git = repo.git
        git.checkout("master")
        repo.remotes[0].pull()
    return repo


# returns a new session
def connect(host="localhost", port=9042, keyspace=None, graph=False):
    setup([host], keyspace)
    return get_db_session()

def create_keyspace():
    # TODO ask for strategy and RF
    print "Creating keyspace (SimpleStrategy)"
    print "Replication factor 1"
