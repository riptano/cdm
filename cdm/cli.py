"""cdm - Cassandra Data Manager

Usage:
    cdm search [<term>]
    cdm list [<term>]
    cdm show <dataset>
    cdm install [--host=<host>] [--keyspace=<keyspace>] [--dry-run] <dataset>
    cdm update

Examples:
    cdm install medialens
"""

import sys
sys.path.append("")
import os
import os.path
import urllib2
import subprocess

# 3rd party
import yaml
from git import Repo

from docopt import docopt
from cassandra.cluster import Cluster


DEBUG = False
DATASETS_URL = "https://raw.githubusercontent.com/cassandra-data-manager/cdm/master/datasets.yaml"

CDM_CACHE = os.getenv("CDM_CACHE", os.path.expanduser("~/.cdm/"))
CDM_PACKAGE_FILE = CDM_CACHE + "datasets.yaml"

def main():
    arguments = docopt(__doc__)
    print arguments
    # print arguments

    try:
        os.mkdir(CDM_CACHE)
    except OSError:
        pass


    if arguments["search"] or arguments["list"]:
        return list_datasets(arguments["<term>"])

    if arguments["update"]:
        return update_datasets()

    if arguments["install"]:
        tmp = arguments["<dataset>"].split("==")
        if len(tmp) == 1: tmp.append("master")
        return install(tmp[0], tmp[1])

    if arguments["show"]:
        return show_dataset_details(arguments["<dataset>"])

    print "Done"

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

def install(dataset, version="master"):
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

    # load the schema
    schema = local_dataset_path(dataset) + "/schema.cql"

    # i'm so sorry for the following code...
    print "Applying schema {}".format(schema)
    command = "cqlsh -k {} -f {} ".format(dataset, schema)
    print command
    subprocess.call(command, shell=True)



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


if __name__ == "__main__":
    main()
