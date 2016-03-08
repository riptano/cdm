.. role:: bash(code)
:language: bash

Creating Datasets
==================

Dataset Directory Structure
--------------------------------

The following skeleton directory structure is required::

    /install.py
    /tests
    schema.cql

Sometime in the future, :bash:`cdm new` will be able to generate a skeleton project.

Testing
-------

Testing datasets is important.  This project is leveraging features of py.test that make it easy to test datasets.

Installers
-----------

Installers are created by having a file called :code:`install.py` in the top level of your dataset.  The installer must subclass :code:`cdm.installer.Installer`.  The cdm utility will discover the Installer automatically so the name is somewhat arbitrary, however it should reflect the dataset's name as a convention.

Cassandra Schema
-------------------


DSE Search Schema
-----------------


DSE Graph
-----------

Graph support can be activated by the :bash:`--graph` command line switch.  If this switch is supplied, your Installer's :code:`install_graph()` method will be called.  If it is not implemented the user will receive an error.

