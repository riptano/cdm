"""cdm - Cassandra Data Manager

Usage:
    cdm list
    cdm versions <dataset>
    cdm install [--host=<host>] [--keyspace=<keyspace>] [--dry-run] <dataset>
    cdm update

Examples:
    cdm install medialens
"""

import sys
sys.path.append("")
from docopt import docopt

DEBUG=False

def main():
    arguments = docopt(__doc__)
    print arguments

    if arguments["list"]: return list_datasets()
    if arguments["update"]: return update_datasets()

    print "Done"

def list_datasets():
    print "Available datasets:"

def update_datasets():
    print "Updating datasets"

if __name__ == "__main__":
    main()
