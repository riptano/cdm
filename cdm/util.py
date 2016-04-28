import os
import os.path
import subprocess
import urllib2
import logging
import yaml
from git import Repo
from importlib import import_module
from shutil import copytree, rmtree
from cassandra.cqlengine.connection import setup, get_session as get_db_session

# try to import the dse session
# if it works, monkey patch cqlengine to use dse session

from cdm.util import *
from cdm.context import Context
from cdm.installer import Installer
import sys
from distutils.spawn import find_executable
import yaml
DATASETS_URL = "https://raw.githubusercontent.com/riptano/cdm/master/datasets.yaml"

CDM_CACHE = os.getenv("CDM_CACHE", os.path.expanduser("~/.cdm/"))
CDM_PACKAGE_FILE = CDM_CACHE + "datasets.yaml"

logger = logging.getLogger(__name__)

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
        logger.info("No datasets found")


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
    cql = "drop keyspace if exists {}".format(keyspace)
    session.execute(cql)

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
    # if (install_graph or install_search) and not find_executable("dsetool"):
    #     print "DSE features requested but DSE bin not in PATH"
    #     sys.exit(1)

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

        tutorials_root_dir = os.path.join(CDM_CACHE, "tutorials")

        if not os.path.exists(tutorials_root_dir):
            logger.info("Creating tutorials directory")
            os.mkdir(tutorials_root_dir)

        logger.info("Setting up tutorials")
        dest = os.path.join(tutorials_root_dir, dataset)

        if os.path.exists(dest):
            logger.info("Clearing out old tutorial directory")
            rmtree(dest)

        copytree(os.path.join(path, "tutorials"), dest)

    # install requirements.  need to come back to this.
    # req_file = os.path.join(path, "requirements.txt")
    # if os.path.exists(req_file):
    #     print "Installing requirements"
    #     subprocess.check_call(["pip", "install", "-r", req_file])

    print "Connecting"

    session = get_session(dataset, install_graph, host=host)
    # load the schema

    if not os.path.exists(cache_dir):
        os.mkdir(cache_dir)

    context = Context(root=path,
                      dataset=dataset,
                      session=session,
                      cache_dir=cache_dir)


    # move to context
    installer = context.installer
    installer._cassandra = install_cassandra
    installer._search = install_search
    installer._graph = install_graph
    installer._install()



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


def prompt(p, default):
    command = "{} [{}]>".format(p, default)
    result = raw_input(command).strip()
    return result if result else default


def configure_config(fp):
    cassandra_host = prompt("Cassandra host?", "localhost")
    spark_host = prompt("Spark host?", "localhost")

    # write config out
    data = {"cassandra_host": cassandra_host,
            "spark_host": spark_host }

    fp.write(yaml.dump(data, default_flow_style=False))

