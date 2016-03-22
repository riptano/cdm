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

Want to get up and running?  See the :doc:`/quickstart`


User Documentation
-------------------

.. toctree::
   :maxdepth: 2

   quickstart
   usage
   faq

Developer Documentation
-----------------------

.. toctree::
   :maxdepth: 2

   datasets


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

