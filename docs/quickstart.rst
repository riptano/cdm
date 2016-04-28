QuickStart
============

Make sure you have either open source Cassandra (2.1 or later) or DataStax Enterprise (4.8 or greater) installed.

Getting up and running with CDM is simple.  In a virtualenv, run the following::

    pip install cassandra-dataset-manager

You'll have a command line utility, :code:`cdm`, installed in your virtualenv's bin directory.  Update your local dataset list, then install the movielens-small dataset::

    cdm update
    cdm install movielens-small

You now have the `movielens-small` dataset installed in your local cassandra cluster.

Next, type `cqlsh` to start working with the Cassandra shell.

Once cqlsh starts, type `use movielens_small` then `desc tables` to see all the tables in the schema.  Type the following to read some data:




