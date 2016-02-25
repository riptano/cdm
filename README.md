# Cassandra Data Manager

Tool for installing cassandra datasets.

This repository contains the cdm tool only.  Other repositories in this repo contain the actual datasets.

## Installation

`pip install cassandra-data-manager`

## Usage

cdm install [dataset]

## Requesting a dataset

Please submit a GitHub issue requesting the dataset, with as much detail as possible.  You should include the following:

* Dataset URL
* What you'd like to use the data for


## Repository Layout Specification

schema.cql will be run in the keyspace.

data.cql will be run in the keyspace also.

post_install.cql will be run after data.cql is imported.  this is preferred if there's a lot of data that might need to be downloaded from an external source.

## Contributing

See the contributing doc.   





## Generating a new dataset
