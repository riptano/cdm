from pytest  import fixture
from cdm.testing import get_context

# returns a sample application
@fixture(scope="session")
def sample():
    context = get_context()

