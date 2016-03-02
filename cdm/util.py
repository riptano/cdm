import os
import os.path
import subprocess
import urllib2

import yaml
from git import Repo
from importlib import import_module
from cassandra.cqlengine.connection import setup, get_session as get_db_session
from cdm.util import *
from cdm.context import Context
import imp
import inspect
from cdm.installer import Installer

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

def get_session(dataset):
    keyspace = normalize_dataset_name(dataset)
    session = connect(keyspace=keyspace)

    print "Creating keyspace"
    if keyspace not in session.cluster.metadata.keyspaces:
        cql = "create KEYSPACE {} WITH replication = {{'class': 'SimpleStrategy', 'replication_factor': 1}}".format(keyspace)
        session.execute(cql)

    session.set_keyspace(keyspace)
    return session

def install(dataset, version="master", install_graph=False, install_search=False):
    print "Installing dataset {}=={}".format(dataset, version)
    y = open_datasets()

    # returns the git repo
    repo = download_dataset(dataset, y[dataset]['url'])
    # we should be on master now
    # do I need a specific version?
    repo.git.checkout(version)

    print "Connecting"
    session = get_session(dataset)
    # load the schema
    schema = local_dataset_path(dataset) + "/schema.cql"
    keyspace = normalize_dataset_name(dataset)

    cache_dir = CDM_CACHE + dataset + "_cache"
    if not os.path.exists(cache_dir):
        os.mkdir(cache_dir)

    context = Context(root=local_dataset_path(dataset),
                      dataset=dataset,
                      session=session,
                      cache_dir=cache_dir)

    # post_install = imp.load_source("{}.main".format(name), post_install_script)
    post_install = local_dataset_path(dataset) + "/install.py"
    context.feedback("Loading installer {}".format(post_install))
    module = imp.load_source("Installer", post_install)
    members = inspect.getmembers(module)

    matching = [c for (name, c) in members if isinstance(c, type)
                                            and c is not Installer
                                            and issubclass(c, Installer)]
    if not matching:
        raise InstallerNotFound()


    installer = matching[0](context)
    installer.install()



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
def connect(host="localhost", port=9042, keyspace=None):
    setup([host], keyspace)
    # session = Cluster([host]).connect()
    return get_db_session()

def create_keyspace():
    # TODO ask for strategy and RF
    print "Creating keyspace (SimpleStrategy)"
    print "Replication factor 1"
