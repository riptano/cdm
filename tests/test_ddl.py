from pytest import fixture
from cdm.ddl import parse_line, create_vertex

def test_create_property():
    result = parse_line("CREATE PROPERTY name text")


def test_create_vertex_label():
    cmd = "CREATE vertex movie"
    result = create_vertex.parseString(cmd)
    import ipdb; ipdb.set_trace()
    result = parse_line(cmd)
    result2 = parse_line("CREATE vertex label movie")

def test_create_edge_label():
    result = parse_line("CREATE edge rated")
    result2 = parse_line("CREATE edge label rated")


def test_create_index_fulltext():
    result = parse_line("CREATE INDEX search on movie(title) FULLTEXT")

def test_create_index_materialize():
    result = parse_line("CREATE INDEX movie_title_idx ON movie(title) SEARCH");
    result = parse_line("CREATE INDEX user_id_idx ON movie(user_id) MATERIALIZED")
