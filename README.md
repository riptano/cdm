# Cassandra Data Manager

Tool for installing cassandra datasets.  This is not a bulk loader.  It is intended to be used as a tool for learning and educational purposes.

This repository contains the cdm tool only, and has references to repositories which are independently maintained.

## Installation

`pip install cassandra-dataset-manager`
    
The project is still under heavy development, a lot is changing very quickly.

## Quickstart

Let's install the movielens-small dataset.  It's a quick download at just a few MB and gives you a database you can play with.

    cdm update
    cdm install movielens-small
    
Open the Cassandra shell:
       
    cqlsh -k movielens_small 
    desc tables;
    select * from movies limit 10;
    
Options are all available at `cdm help`

I encourage you to read through the [documentation](http://cdm.readthedocs.org/en/latest/).
    
