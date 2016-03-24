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

Download resources and setup
-------------------------------

Set up your :code:`post_init()` hook.  You should download and load any data into memory you'll need for all the various imports::

    class MovieLensInstaller(Installer):
        def post_init(self):
            context = self.context
            self.my_data = some_helper()

If you need to download any data (like a zip file of CSVs, etc), you can use :code:`context.download(url)` which will download and cache the file at the URL return a file pointer.  Caching is provided automatically.

If you download a zip file, the easiest way to access the data is using the built in Python ZipFile module::

    fp = context.download("http://files.grouplens.org/datasets/movielens/ml-100k.zip")
    zf = ZipFile(file=fp)
    fp = zf.open("ml-100k/u.item")

You can use the file pointers returned from :code:`ZipFile.open(name)` as normal pointers.  If you're working with CSV data, it's recommended to use the Pandas library (provided by CDM)::

    movies = read_csv(fp, sep="|", header=None, index_col=0, names=["id", "name", "genre"]).fillna(0)

You can see how it's pretty easy to use the :code:`Context` to download and cache external files, then process and prepare using Pandas.

Set up Cassandra Schema
------------------------

Next you'll want to set up a schema for Cassandra.  There's a few options varying in complexity.  Read up on the different options for configuring your :doc:`/schema/cassandra`.

Load Cassandra Data
---------------------

Assuming you've loading some data into memory in the :code:`post_init()`, you can now load data into your schema.

To load data, you'll want to use the :code:`session` provided by the :code:`Context`::

    class MyInstaller(Installer):
        def install_cassandra(self):
            context = self.context
            session = context.session
            prepared = session.prepare("INSERT INTO data (key, value) VALUES (?, ?)")
            for row in self.data:
                session.execute(prepared, row.key, row.value)



DSE Search Schema
------------------

An installer can provide search functionality.  A user may enable search with the :code:`--search` flag.

*Note: This feature is still in early development.*

Providing a search schema will be managed through the :code:`Installer.search_schema()` method.  It's exact behavior is still undefined.

Since integrated search is provided automatically there is no hook to install search data.

DSE Graph Schema
-----------------

Graph support can be activated by the :bash:`--graph` command line switch.  If this switch is supplied, your Installer's :code:`install_graph()` method will be called.  If it is not implemented the user will receive an error.

*Note: This feature is still in early development.*

Providing a graph schema will be managed through the :code:`Installer.graph_schema()` method.  It's exact behavior is still undefined.

DSE Graph Data
---------------

Let's look at an example::

    class MyInstaller(Installer):
        def install_graph(self):
            # create movies
            session = self.context.session
            from dse.graph import SimpleGraphStatement

            movie_stmt = SimpleGraphStatement("graph.addVertex(label, 'movie', 'name', name, 'id', movie_id)")

            for movie in self.movies.itertuples():
                params = {"name": movie.name,
                          "movie_id": movie.Index}
                session.execute_graph(movie_stmt, params)


Provided Libraries
-------------------

Cassandra Driver
    The project would be useless without a driver, so it's included.  We will stay reasonably up to date with current packages.  It is always made available via the :doc:`/context` as the :code:`session` variable.

Pandas
    Pandas is an excellent library for reading various raw formats such as CSV.  It also provides facilities for data manipulation, which may be required to transform data.

Faker
    Faker makes for each generation of fake data.  This is especially useful when you're dealing with an incomplete data model or one that has been anonymized.

Firehawk
    Firehawk is an experimental library that translates schema shorthand to DSE Graph groovy functions.


Testing
-------

Testing datasets is important.  This project is leveraging features of py.test that make it easy to test datasets.

CDM will include a tool for testing a project.  This runs all the projects unit tests as well as tests that verify project structure and conventions::

    cdm test

All tests must pass :code:`cdm test` for inclusion in the official Dataset repository.
