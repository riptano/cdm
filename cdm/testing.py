import pytest
import os
from os.path import join
from cdm import get_session
from cdm.context import Context


@pytest.fixture(scope="session")
def context():
    """
    returns a context with a whole bunch of stuff set up
    :return:
    """

    def fin():
        print "Teardown context"

    cache_dir = join(os.getcwd(), ".cdmcache")
    try:
        os.mkdir(cache_dir)
    except:
        # TODO don't be so silly
        pass

    c = Context(root=os.getcwd(),
                dataset="test",
                session=get_session("test", True),
                cache_dir=cache_dir)

    return c
