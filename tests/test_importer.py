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

@fixture
def importer(df, session):
    return Importer(session, df)


def test_simple_transform(session, df):
    i = Importer(session, df)
    row = i.iter().next()
    assert isinstance(row, dict)
    assert row['name'] == "Jon"

def test_custom_transform(session, df):
    def t(row):
        row['name'] = row['name'].upper()
        return dict(row)

    i = Importer(session, df, transformation=t)
    row = i.iter().next()
    assert isinstance(row, dict)
    assert row['name'] == "JON"


def test_insert_statement(importer):
    row = importer.iter().next()
    stmt, values = importer.get_insert(row, "tab")
    assert stmt.startswith("INSERT INTO tab")


def test_load(importer):
    queries = ["DROP TABLE IF EXISTS test_importer",
               "CREATE TABLE test_importer (name text primary key, hats int, nickname text)"]

    for q in queries:
        importer.session.execute(q)

    importer.load("test_importer")
