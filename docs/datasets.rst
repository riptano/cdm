.. role:: bash(code)
:language: bash

Guide: Creating Datasets
========================

This information is relevant only to developers wishing to create their own datasets for distribution.

What is a Dataset?
------------------

Think of a Dataset similar to a package managed by yum or apt.  Instead of binaries and configuration files, installing a Dataset gives you a Cassandra schema, sample data, and a Jupyter notebook with tutorials on how to use that data.

Create a new project from the skeleton
---------------------------------------

Make sure CDM is installed.  You will not be able to provide additional Python modules other than what CDM already provides (yet).

Create a new dataset with the :bash:`cdm new` command.  It will generate a project skeleton for you.  For example::

    cdm new example-name


Installers are created by having a file called :code:`install.py` in the top level of your dataset.  The installer must subclass :code:`cdm.installer.Installer`.  The cdm utility will discover the Installer automatically so the name is somewhat arbitrary, however it should reflect the dataset's name as a convention.

Configure your post_init
--------------------------

Set up your :code:`post_init()` hook.  You should load any data you'll need for all the various imports::

    class MovieLensInstaller(Installer):
        def post_init(self):
            context = self.context
            self.my_data = some_helper()

If you need to download any data (like a zip file of CSVs, etc), you can use context.download(url) which will return a file pointer.

Set up Cassandra Schema
------------------------

Read up on the different options for configuring your :doc:`/schema/cassandra`.

Load Cassandra Data
---------------------

Assuming you've loading some data into memory in the :code:`post_init()`, you can now load data into your schema.

Loading data::

    class MyInstaller(Installer):
        def install_cassandra(self):
            context = self.context
            session = context.session()
            prepared = session.prepare("INSERT INTO data (key, value) VALUES (?, ?)")
            for row in self.data:
                session.execute(prepared, row.key, row.value)


Provided Libraries
-------------------

Cassandra Driver
    The project would be useless without a driver, so it's included.  We will stay reasonably up to date with current packages.  It is always made available via the :doc:`/context` as the :code:`session` variable.

Pandas
    Pandas is an excellent library for reading various raw formats such as CSV.  It also provides facilities for data manipulation, which may be required to transform data.

Faker
    Faker makes for each generation of fake data.  This is especially useful when you're dealing with an incomplete data model or one that has been anonymized.


Hooks
------

A number of hooks are available.

Dataset Directory Structure
--------------------------------

The following skeleton directory structure is required::

    /install.py
    /tests
    schema.cql


Testing
-------

Testing datasets is important.  This project is leveraging features of py.test that make it easy to test datasets.

CDM will include a tool for testing a project.  This runs all the projects unit tests as well as tests that verify project structure and conventions::

    cdm test

All tests must pass :code:`cdm test` for inclusion in the official Dataset repository.



DSE Search
----------

An installer can provide search functionality.  A user may enable search with the :code:`--search` flag.

DSE Graph
-----------

Graph support can be activated by the :bash:`--graph` command line switch.  If this switch is supplied, your Installer's :code:`install_graph()` method will be called.  If it is not implemented the user will receive an error.

