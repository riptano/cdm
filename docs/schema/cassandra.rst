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

This is a convenient as you'll frequently want to

Explicitly Using Strings
-------------------------

This will be necessary for UDAs/UDFs as they aren't simply split on :code:`;`.  A future version of CDM may include a parser to properly support this but it's unlikely anytime soon.

Mixed
-----
