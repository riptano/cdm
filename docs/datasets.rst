.. role:: bash(code)
:language: bash

Creating Datasets
==================

Make sure CDM is installed.  You will not be able to provide additional Python modules other than what CDM already provides (yet).

Create a new dataset with the :bash:`cdm new` command.  It will generate a project skeleton for you.  For example::

    cdm new example-name

Provided Libraries
-------------------

Cassandra Driver
    The project would be useless without a driver, so it's included.  We will stay reasonably up to date with current packages.  It is always made available via the :doc:`/context`.

Pandas
    Pandas is an excellent library for reading various raw formats such as CSV.  It also provides facilities for data manipulation, which may be required to transform data.

Faker
    Faker makes for each generation of fake data.  This is especially useful when you're dealing with an incomplete data model or one that has been anonymized.



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

