.. Cassandra Dataset Manager documentation master file, created by
   sphinx-quickstart on Tue Mar  1 20:50:55 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Cassandra Dataset Manager
==========================

Cassandra Dataset Manager, (cdm) is a tool to make it simple to start learning Apache Cassandra or Datastax Enterprise (DSE).  This utility will provide a framework for building and installing datasets, which can then be explored via cqlsh, DevCenter, and the Jupyter notebooks that are included with datasets.  In short, the focus of this tool is on the following:

Development of Datasets
    The CDM framework will provide a consistent experience for people interested in sharing public datasets.

Installation of Datasets
    It should take 15 minutes or less for a user to go from "I want to learn" to "I'm looking at data".  The experience of loading sample data should be as simple as possible, with helpful error messages when things do go wrong or a requirement it not installed.

Visual Learning via Examples
    Jupyter notebooks provide an elegant means of teaching database and data model concepts by interweaving explanatory text and executable code.  The CDM framework will provide convenient means of displaying information from Cassandra and DSE Search.


Things this is not
-------------------

1. A bulk loader
2. A way for you to manage your schema in your projects

QuickStart
----------

Make sure you have either open source Cassandra (2.1 or later) or DataStax Enterprise (4.8 or greater) installed.

Getting up and running with CDM is simple.  In a virtualenv, run the following::

    pip install -e git+https://github.com/cassandra-dataset-manager/cdm.git#egg=cdm

You'll have a command line utility, :code:`cdm`, installed in your virtualenv's bin directory.  Update your local dataset list, then install the movielens-small dataset::

    cdm update
    cdm install movielens-small

You can now learn about this dataset by running::

    cdm tutorials movielens-small

This will open a Jupyter notebook with various tutorials about the data model and code examples.  For more information, consult the usage section of the documentation.

Full Documentation
-------------------

.. toctree::
   :maxdepth: 2

   usage
   datasets
   faq



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

