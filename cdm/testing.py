import pytest

@pytest.fixture
def context():
    """
    returns a context with a whole bunch of stuff set up
    :return:
    """
    def fin():
        print "Teardown context"
