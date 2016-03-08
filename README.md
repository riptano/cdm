# Cassandra Data Manager

Tool for installing cassandra datasets.

This repository contains the cdm tool only.  Other repositories in this repo contain the actual datasets.

## Installation

`pip install cassandra-dataset-manager`

Clone the repo.  Using a visualenv:

    python setup.py develop
    
The project is still under heavy development, a lot is changing very quickly.

## Quickstart

Let's install the movielens-small dataset.  It's a quick download at just a few MB and gives you a database you can play with.

    cdm update
    cdm install movielens-small
    
Options are all available at `cdm help`

I encourage you to read through the [documentation](http://cdm.readthedocs.org/en/latest/).
    

## Requesting a dataset

Please submit a GitHub issue requesting the dataset, with as much detail as possible.  You should include the following:

* Dataset URL
* What you'd like to use the data for (so we can structure tables accordingly)




