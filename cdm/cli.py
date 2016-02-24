"""cdm - Cassandra Data Manager

Usage:
    cdm search [<term>]
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

DEBUG = False
DATASETS_URL = "https://github.com/cassandra-data-manager/cdm/blob/master/datasets.yaml"

CDM_CACHE = os.getenv("CDM_CACHE", os.path.expanduser("~/.cdm"))

def main():
    arguments = docopt(__doc__)
    print arguments

    try:
        os.mkdir(CDM_CACHE)
    except OSError:
        pass


    if arguments["search"]: return list_datasets(arguments["<term>"])
    if arguments["update"]: return update_datasets()

    print "Done"

def list_datasets(search):
    print "Available datasets:"

def update_datasets():
    print "Updating datasets"


if __name__ == "__main__":
    main()
