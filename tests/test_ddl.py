from pytest import fixture
from cdm.ddl import parse_line, create_vertex, create_index,\
                    CreateVertex, \
                    CreateEdge, CreateProperty, CreateIndex, CreateGraph


def test_create_graph():
    s = "CREATE GRAPH jon"
    parsed = parse_line(s)
    assert isinstance(parsed, CreateGraph)
    assert "system.createGraph('jon').build()" in str(parsed)

def test_create_vertex_label():
    cmd = "CREATE vertex movie"
    result = create_vertex.parseString(cmd)[0]
    assert isinstance(result, CreateVertex)

    result = parse_line(cmd)
    assert isinstance(result, CreateVertex)
    assert result.label == "movie"

    result2 = parse_line("CREATE vertex label movie")
    assert isinstance(result, CreateVertex)

def test_create_edge_label():
    result = parse_line("CREATE edge rated")
    assert isinstance(result, CreateEdge)
    assert result.label == "rated"
    result2 = parse_line("CREATE edge label rated")


def test_create_property():
    result = parse_line("CREATE PROPERTY name text")
    assert isinstance(result, CreateProperty)


def test_create_index_fulltext():
    s = "CREATE VERTEX INDEX search on movie(title) FULLTEXT"
    result = create_index.parseString(s)

#     result = parse_line()
#     assert isinstance(result, CreateIndex)
#
# def test_create_index_materialize():
#     result = parse_line("CREATE INDEX movie_title_idx ON movie(title) SEARCH");
#     result = parse_line("CREATE INDEX user_id_idx ON movie(user_id) MATERIALIZED")
