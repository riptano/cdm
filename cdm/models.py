from cassandra.cqlengine.models import Model
from cassandra.cqlengine.columns import *

class Source(Model):
    name = Text(primary_key=True)
    url = Text()

class Dataset(Model):
    source = Text(primary_key=True)
    name = Text(primary_key=True)
    hash_installed = Text()
