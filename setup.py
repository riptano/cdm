from distutils.core import setup
from setuptools import find_packages

setup(
        name='Cassandra Data Manager',
        version='0.1',
        packages=['cdm'],
        url='https://github.com/cassandra-data-manager/cdm',
        license='License :: OSI Approved :: BSD License',
        author='Jon Haddad',
        author_email='jon@jonhaddad.com',
        description='Utility for quickly setting up sample datasets for Cassandra',
        entry_points={
            'console_scripts': [
                'cdm=cdm.cli:main'
            ]
        },
        install_requires=[
            "cassandra-driver"
        ]

)
