QuickStart
============

Make sure you have either open source Cassandra (2.1 or later) or DataStax Enterprise (4.8 or greater) installed.

Getting up and running with CDM is simple.  In a virtualenv, run the following::

    pip install -e git+https://github.com/cassandra-dataset-manager/cdm.git#egg=cdm

You'll have a command line utility, :code:`cdm`, installed in your virtualenv's bin directory.  Update your local dataset list, then install the movielens-small dataset::

    cdm update
    cdm install movielens-small

You can now learn about this dataset by running::

    cdm tutorials movielens-small

This will open a Jupyter notebook with various tutorials about the data model and code examples.  For more information, consult the :doc:`/usage` section of the documentation.
