from cdm.importer import Importer
from pandas import DataFrame
from pytest import fixture
from cdm.importer import Importer
from cdm.testing import session

@fixture
def df():
    data = [{'name': "Jon", 'hats': 1,
             'nickname':"Beast"},
            {'name': "Luke", 'hats': 50,
             'nickname':"Loopsie"}]

    return DataFrame(data)



def test_simle_transform(session, df):
    i = Importer(session, df)
    row = i.iter().next()
    assert isinstance(row, dict)
    assert row['name'] == "Jon"



