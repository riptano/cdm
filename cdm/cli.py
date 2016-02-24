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
import yaml
from git import Repo

from docopt import docopt


DEBUG = False
DATASETS_URL = "https://raw.githubusercontent.com/cassandra-data-manager/cdm/master/datasets.yaml"

CDM_CACHE = os.getenv("CDM_CACHE", os.path.expanduser("~/.cdm/"))
CDM_PACKAGE_FILE = CDM_CACHE + "datasets.yaml"

def main():
    arguments = docopt(__doc__)
    # print arguments

    try:
        os.mkdir(CDM_CACHE)
    except OSError:
        pass


    if arguments["search"] or arguments["list"]: return list_datasets(arguments["<term>"])
    if arguments["update"]: return update_datasets()
    if arguments["install"]: return install(arguments["<dataset>"])

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

def install(dataset):
    print "Installing dataset"
    y = open_datasets()
    download_dataset(dataset, y[dataset]['url'])


def download_dataset(dataset_name, dataset_url):
    local_git = CDM_CACHE + dataset_name
    if not os.path.exists(local_git):
        repo = Repo.clone_from(dataset_url, local_git)
        print "Downloaded"
    else:
        print "Repo exists, pulling latest"
        repo = Repo(local_git)
        repo.remotes[0].pull()


    print repo



if __name__ == "__main__":
    main()
