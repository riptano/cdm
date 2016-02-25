import os
import os.path


from git import Repo
from importlib import import_module
from docopt import docopt
import subprocess
import yaml
from cassandra.cluster import Cluster
from cdm.util import *
from cdm.context import Context
import imp
DATASETS_URL = "https://raw.githubusercontent.com/cassandra-data-manager/cdm/master/datasets.yaml"

CDM_CACHE = os.getenv("CDM_CACHE", os.path.expanduser("~/.cdm/"))
CDM_PACKAGE_FILE = CDM_CACHE + "datasets.yaml"

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

def install(dataset, version="master", install_graph=False, install_search=False):
    print "Installing dataset {}=={}".format(dataset, version)
    y = open_datasets()

    # returns the git repo
    repo = download_dataset(dataset, y[dataset]['url'])
    # we should be on master now
    # do I need a specific version?
    repo.git.checkout(version)

    print "Connecting"
    session = connect()

    print "Creating keyspace"
    if dataset not in session.cluster.metadata.keyspaces:
        cql = "create KEYSPACE {} WITH replication = {{'class': 'SimpleStrategy', 'replication_factor': 1}}".format(dataset)
        session.execute(cql)

    session.set_keyspace(dataset)
    # load the schema
    schema = local_dataset_path(dataset) + "/schema.cql"

    # i'm so sorry for the following code...
    print "Applying schema {}".format(schema)
    command = "cqlsh -k {} -f {} ".format(dataset, schema)
    print command
    subprocess.call(command, shell=True)
    # check for CQL file loading options?
    # check for python loading options
    cache_dir = CDM_CACHE + dataset + "_cache"
    os.mkdir(cache_dir)

    context = Context(dataset=dataset,
                      session=session,
                      cache_dir=cache_dir)

    post_install_script = local_dataset_path(dataset) + "/post_install.py"
    # run the post_install.py:main() if it exists
    if os.path.exists(post_install_script): # gross
        print "Running post install script"
        post_install = imp.load_source("post_install.main", post_install_script)
        post_install.main(context)
        print "Post install done."

    if install_search:
        post_install_script = local_dataset_path(dataset) + "/post_install_search.py"
        # run the post_install.py:main() if it exists
        if os.path.exists(post_install_script): # gross
            print "Running post install search script"
            post_install = imp.load_source("post_install_search.main", post_install_script)
            post_install.main(context)
            print "Post install done."

    if install_graph:
        post_install_script = local_dataset_path(dataset) + "/post_install_graph.py"
        # run the post_install.py:main() if it exists
        if os.path.exists(post_install_script): # gross
            print "Running post install script"
            post_install = imp.load_source("post_install_graph.main", post_install_script)
            post_install.main(context)
            print "Post install done."


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


# returns a new Cluster
def connect(host="localhost", port=9042, keyspace=None):
    return Cluster([host]).connect()

def create_keyspace():
    # TODO ask for strategy and RF
    print "Creating keyspace (SimpleStrategy)"
    print "Replication factor 1"
