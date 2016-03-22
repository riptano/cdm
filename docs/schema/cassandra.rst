Cassandra Schema
==================

Working with a Cassandra schema is very flexible using CDM.  There are several options available.

Using a schema file
---------------------

This is useful if you have a schema somewhere already that you want to write to disk through cqlsh, and you don't wish to use CQLEngine models.

To easily use a schema file, make sure your :doc:`installer` subclasses :code:`SimpleCQLSchema`::

    class MyInstaller(Installer, SimpleCQLSchema):
        pass

Put your schema in schema.cql, and it will automatically be picked up and loaded, splitting the statements on :code:`;`;

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


    class MovieLensInstaller(Installer):
        def cassandra_schema(self):
            return [Movie]




Explicitly Using Strings
-------------------------

This will be necessary for UDAs/UDFs as they aren't simply split on :code:`;`.  A future version of CDM may include a parser to properly support this but it's unlikely anytime soon.

Mixed
-----
