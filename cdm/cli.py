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
from docopt import docopt
import urllib2


DEBUG = False
DATASETS_URL = "https://raw.githubusercontent.com/cassandra-data-manager/cdm/master/datasets.yaml"

CDM_CACHE = os.getenv("CDM_CACHE", os.path.expanduser("~/.cdm/"))


def main():
    arguments = docopt(__doc__)
    print arguments

    try:
        os.mkdir(CDM_CACHE)
    except OSError:
        pass


    if arguments["search"] or arguments["list"]: return list_datasets(arguments["<term>"])
    if arguments["update"]: return update_datasets()

    print "Done"

def list_datasets(search):
    print "Available datasets:"

def update_datasets():
    print "Updating datasets"
    fp = urllib2.urlopen(DATASETS_URL)
    data = fp.read()
    print data

    with open(CDM_CACHE + "datasets.yaml", 'w') as d:
        d.write(data)




if __name__ == "__main__":
    main()
