Context
=======

A Context provides useful information and database functionality automatically for the developer.  There is no need to select a keyspace, this has been done for you already.


Downloading and Caching Files
------------------------------

The context provides the means of downloading and caching files without having to worry about directory management.  This will be used by any dataset not exclusively generating data.  A file handle is returned to the user.

An example from the movielens-small dataset::

    fp = context.download("http://files.grouplens.org/datasets/movielens/ml-100k.zip")


Working with Zip Files
------------------------

Working with Zip files from a context is trivial via the built in Python ZipFile class::

    from zipfile import ZipFile
    fp = context.download("http://files.grouplens.org/datasets/movielens/ml-100k.zip")
    zf = ZipFile(file=fp)
    fp = zf.open("ml-100k/u.item")

