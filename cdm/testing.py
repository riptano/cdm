import pytest
import os
from os.path import join
from cdm import get_session
from cdm.context import Context


def get_context(path):
    cache_dir = join(os.getcwd(), ".cdmcache")

    try:
        os.mkdir(cache_dir)
    except Exception as e:
        # TODO don't be so silly
        print e

    c = Context(root=path,
                dataset="test",
                session=get_session("test", True),
                cache_dir=cache_dir)
    return c


@pytest.fixture(scope="session")
def context():
    """
    returns a context with a whole bunch of stuff set up
    :return:
    """

    def fin():
        print "Teardown context"

    return get_context(os.getcwd())


def get_sample_context():
    sample = os.path.join(os.getcwd(), "tests/sample")
    return get_context(sample)
