"""
notebook extension for all magic we need for tutorials
"""
from IPython.core.magic import Magics, magics_class, cell_magic, line_magic, needs_local_scope
from IPython.config.configurable import Configurable
from cassandra.cluster import Cluster
from cassandra.query import ordered_dict_factory, SimpleStatement



def load_ipython_extension(ipython):

    global cluster, session

    cluster = Cluster()
    session = cluster.connect()
    session.row_factory = ordered_dict_factory

    ipython.register_magics(CQLMagic)

