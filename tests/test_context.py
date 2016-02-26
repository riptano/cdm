import os
from pytest import fixture

from cdm.context import Context
from cassandra.clusterny import Cluster

session = None

@fixture
def context():
    global session
    if not session:
        cluster = Cluster()
        session = cluster.connect()

        # create the keyspace
        ks = 'test_cdm'
        if 'test_cdm' not in cluster.metadata.keyspaces:
            q = "create KEYSPACE {} WITH \
                    replication = {{'class': \
                    'SimpleStrategy', \
                    'replication_factor': 1}}".format(ks)
            session.execute(q)
        if not os.path.exists("./cache"):
            os.mkdir("./cache")
        session.set_keyspace(ks)

    return Context(dataset="test",
                   session=session,
                   cache_dir="./cache")



def test_download(context):
    context.clean_cache()
    fp = context.download("http://rustyrazorblade.com/pages/about-me.html")

