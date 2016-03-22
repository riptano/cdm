from distutils.core import setup
from setuptools import find_packages

setup(
        name='Cassandra Dataset Manager',
        version='0.1',
        packages=['cdm'],
        url='https://github.com/cassandra-dataset-manager/cdm',
        license='License :: OSI Approved :: BSD License',
        author='Jon Haddad',
        author_email='jon@jonhaddad.com',
        description='Utility for quickly setting up sample datasets for Cassandra and DataStax Enterprise',
        entry_points={
            'console_scripts': [
                'cdm=cdm.cli:main',
                'graph=cdm.graph:main'
            ]
        },
        install_requires=[
            "cassandra-driver>=3.1.0a2", "docopt>=0.6.1",
            "gitpython", "PyYAML", "pandas>=0.17.1",
             "colorama",
            "fake-factory", "requests>=2.9.1"
        ]

)
