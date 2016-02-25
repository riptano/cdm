"""cdm - Cassandra Data Manager

Usage:
    cdm search [<term>]
    cdm list [<term>]
    cdm show <dataset>
    cdm install [--host=<host>] [--keyspace=<keyspace>] [--dry-run] [--graph] [--search] <dataset>
    cdm update

Examples:
    cdm install demo
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
from cdm.util import *

DEBUG = False


def main():
    arguments = docopt(__doc__)
    print arguments

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
        return install(tmp[0], tmp[1],
                       install_graph=arguments['--graph'],
                       install_search=arguments['--search'])


    if arguments["show"]:
        return show_dataset_details(arguments["<dataset>"])

    print "Done"




if __name__ == "__main__":
    main()
