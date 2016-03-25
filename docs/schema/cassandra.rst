Cassandra Schema
==================

Working with a Cassandra schema is very flexible using CDM.  There are several options available.

Using a schema file
---------------------

This is useful if you have a schema somewhere already that you want to write to disk through cqlsh, and you don't wish to use CQLEngine models.

To easily use a schema file, make sure your :doc:`installer` subclasses :code:`SimpleCQLSchema` *first*::

    class MyInstaller(SimpleCQLSchema, Installer):
        pass

Put your schema in schema.cql, and it will automatically be picked up and loaded, splitting the statements on :code:`;`.

CQLEngine Models
------------------

This is a convenient as you'll frequently want to leverage CQLEngine models for validating and inserting data.  We'll use the :code:`cassandra_schema()` hook to return the classes we want sync'ed to the database.

For example, in movielens-small, we define our :code:`Movie` Model similar to this::


    class Movie(Model):
        __table_name__ = 'movies'
        id = Integer(primary_key=True)
        name = Text()
        release_date = Date()
        video_release_date = Date()
        url = Text()
        avg_rating = Float()
        genres = Set(Text)

In our installer, we return a list of table models::

    class MovieLensInstaller(Installer):
        def cassandra_schema(self):
            return [Movie]




Specifying a Schema Inline
-------------------------------

This will be necessary for UDAs/UDFs as they aren't simply split on :code:`;`.  A future version of CDM may include a parser to properly support this but it's unlikely anytime soon.  Until that day comes, it's possible to use fat strings to specify schema::

    class MovieLensInstaller(Installer):
        def cassandra_schema(self):
            statements = ["""CREATE TABLE movies
                            (id uuid primary key,
                             name text)""",
                         """CREATE CUSTOM INDEX on movies(name)
                            USING 'org.apache.cassandra.index.sasi.SASIIndex'"""
            return statements

Mixed Mode
----------

There are cases which are not handled with CQLEngine yet.  Materialized views, SASI indexes, UDFs, UDAs are all difficult to express.  Python allows us a lot of flexibility by allowing lists to contain objects of mixed types.  We can leverage our CQLEngine models for our tables and provide fat strings for the rest of the schema::

    class MovieLensInstaller(Installer):
        def cassandra_schema(self):
            statements = [Movie,
                           """CREATE CUSTOM INDEX on movies(name)
                              USING 'org.apache.cassandra.index.sasi.SASIIndex'"""]

This is cool because we can leverage CQLEngine for our database models but still get the flexibility of using any CQL that it doesn't support yet.
