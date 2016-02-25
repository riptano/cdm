from pytest import fixture

from cdm.context import Context
from cassandra.cluster import Cluster

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

        session.set_keyspace(ks)

    return Context(session=session)





