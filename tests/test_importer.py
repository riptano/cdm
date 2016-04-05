from cdm.importer import Importer
from pandas import DataFrame
from pytest import fixture

@fixture
def df():
    data = [{'name': "Jon", 'hats': 1, 'nickname':"Beast"},
            {'name': "Luke", 'hats': 50, 'nickname':"Loopsie"}]

    return DataFrame(data)


def test_simple_importer(df):
    pass
