from pyparsing import Word, alphas, Keyword, Optional, LineStart, alphanums, oneOf
from collections import namedtuple


CreateVertex = namedtuple("CreateVertex", ["label"])
CreateEdge = namedtuple("CreatedEdge", ["label"])
CreateProperty = namedtuple("CreateProperty", ["name", "type"])
CreateIndex = namedtuple("CreateIndex", ["fields", "type"])

create = Keyword('create', caseless=True)
property = Keyword('property', caseless=True)
vertex = Keyword('vertex', caseless=True)
edge = Keyword('edge', caseless=True)

index = Keyword('index', caseless=True)
label = Keyword('label', caseless=True)
on_ = Keyword("on", caseless=True)
materialized = Keyword("materialized", caseless=True)
fulltext = Keyword("fulltext", caseless=True)

ident =  Word(alphas, alphanums + "_")

typename = oneOf("""ascii bigint blob boolean counter date
                  decimal double float inet int smallint text time
                  timestamp timeuuid tinyint uuid varchar varint""")

create_vertex = (create + vertex + Optional(label) + ident('label')).\
                setParseAction(lambda s, l, t: CreateVertex(label=t.label) )

create_edge = (create + edge + Optional(label) + ident('label')).\
                setParseAction(lambda s, l, t: CreateEdge(label=t.label))

create_property = (create + property + ident("name") + typename("type")).\
                setParseAction(lambda s, l, t: CreateProperty(name=t.name, type=t.type))

# create_index = (create + index + Optional(ident) + )

statement = create_vertex | create_edge | create_property


def parse_line(s):
    """
    parses a single line
    :param s:
    :return:
    """
    return statement.parseString(s)[0]


