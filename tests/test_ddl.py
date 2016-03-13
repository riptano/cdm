from pytest import fixture
from cdm.ddl import parse_line, create_vertex, \
                    create_vertex_index,\
                    CreateVertex, \
                    CreateEdge, CreateProperty, \
                    CreateVertexIndex, \
                    CreateGraph, ShowGraphs, describe_graph, create_edge_index


def test_create_graph():
    s = "CREATE GRAPH jon"
    parsed = parse_line(s)
    assert isinstance(parsed, CreateGraph)
    assert "system.createGraph('jon').build()" in str(parsed)



def test_show_graphs():
    s = "show graphs"
    parsed = parse_line(s)
    assert isinstance(parsed, ShowGraphs)
    assert "system.graphs" in str(parsed)

def test_create_vertex_label():
    cmd = "CREATE vertex movie"
    result = create_vertex.parseString(cmd)[0]
    assert isinstance(result, CreateVertex)

    result = parse_line(cmd)
    assert isinstance(result, CreateVertex)
    assert result.label == "movie"

    assert "buildVertexLabel" in str(result)
    assert "movie" in str(result)

    result2 = parse_line("CREATE vertex label movie")
    assert isinstance(result, CreateVertex)

def test_create_edge_label():
    result = parse_line("CREATE edge rated")
    assert isinstance(result, CreateEdge)
    assert result.label == "rated"
    result2 = parse_line("CREATE edge label rated")
    assert isinstance(result2, CreateEdge)



def test_create_property():
    result = parse_line("CREATE PROPERTY name text")
    assert isinstance(result, CreateProperty)
    result = parse_line("CREATE PROPERTY name TEXT")
    assert isinstance(result, CreateProperty)


"""
graph.schema().vertexLabel("ip").buildVertexIndex("ipById").materialized().byPropertyKey("id").add()
Secondary
graph.schema().vertexLabel("ip").buildVertexIndex("ipByCountry").secondary().byPropertyKey("country").add()
Search
graph.schema().vertexLabel("swid").buildVertexIndex("search").search().byPropertyKey("dob").add()
"""

def test_create_index_fulltext():
    s = "CREATE materialized INDEX movie_title_idx ON VERTEX movie(title )"
    result = create_vertex_index.parseString(s)[0]
    assert result.type == "materialized"
    assert result.label == 'movie'
    assert result.name == 'movie_title_idx'

    groovy = str(result)

    result = parse_line(s)
    s = "CREATE secondary INDEX movie_title_idx ON VERTEX movie(title )"
    result = create_vertex_index.parseString(s)[0]
    assert result.type == "secondary"

    s = "CREATE search INDEX movie_title_idx ON VERTEX movie(title )"
    result = create_vertex_index.parseString(s)[0]
    assert result.type == "search"

    result = parse_line(s)


def test_describe_graph():
    s = "describe graph"
    tmp = describe_graph.parseString(s)[0]
    parse_line(s)


def test_create_edge_index():
    # NOT WORKING, property is on the edge
    # s = "CREATE OUT index ratedbyStars on edge rated(reviewer.stars)"

    s = "CREATE OUT INDEX ratedbyStars ON VERTEX reviewer ON EDGE rated(stars)"
    tmp = create_edge_index.parseString(s)[0]

    assert tmp.edge == "rated"
    assert tmp.direction == "out"
    assert tmp.name == "ratedbyStars"
    assert tmp.vertex == "reviewer"
    assert tmp.property == "stars"

    parse_line(s)
