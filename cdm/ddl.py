from collections import namedtuple

from pyparsing import Word, alphas, Keyword, Optional, LineStart, \
                    alphanums, oneOf, Literal, CaselessLiteral, OneOrMore, delimitedList

class ParsedCommand(object):
    def __init__(self, **kwargs):
        for k, v in kwargs.iteritems():
            self.__setattr__(k, v)

    def to_string(self):
        raise NotImplementedError()

    def __str__(self):
        return self.to_string()

    def execute(self, session):
        s = str(self)
        return session.execute_graph(s)


class CreateVertex(ParsedCommand):
    label = None


class CreateEdge(ParsedCommand):
    label = None


class CreateEdge(ParsedCommand):
    label = None


class CreateProperty(ParsedCommand):
    name = None
    type = None


class CreateIndex(ParsedCommand):
    # element is either vertex or edge
    element = None
    label = None
    fields = None
    type = None

class CreateGraph(ParsedCommand):
    name = None
    def to_string(self):
        return """system.createGraph('{}').build()""".format(self.name)


create = Keyword('create', caseless=True)
property = Keyword('property', caseless=True)
vertex = Keyword('vertex', caseless=True)
edge = Keyword('edge', caseless=True)
graph = Keyword('graph', caseless=True)

index = Keyword('index', caseless=True)
label = Keyword('label', caseless=True)
on_ = Keyword("on", caseless=True).suppress()

materialized = Keyword("materialized", caseless=True)
fulltext = Keyword("fulltext", caseless=True)

index_type = materialized | fulltext

lparen = Literal("(").suppress()
rparen = Literal(")").suppress()

ident =  Word(alphas, alphanums + "_")

typename = oneOf("""ascii bigint blob boolean counter date
                  decimal double float inet int smallint text time
                  timestamp timeuuid tinyint uuid varchar varint""")

create_graph = (create + graph + ident('name')).\
                setParseAction(lambda s,l,t: CreateGraph(name=t.name))

create_vertex = (create + vertex + Optional(label) + ident('label')).\
                setParseAction(lambda s, l, t: CreateVertex(label=t.label) )

create_edge = (create + edge + Optional(label) + ident('label')).\
                setParseAction(lambda s, l, t: CreateEdge(label=t.label))

create_property = (create + property + ident("name") + typename("type")).\
                setParseAction(lambda s, l, t: CreateProperty(name=t.name, type=t.type))

def f(s,l,t):
    return CreateIndex(element=t.element,
                       label=t.label,
                       fields=t.fields,
                       type=t.type)


create_index = (create + (vertex | edge)("element") + index+ Optional(ident)('index_name') +
                on_ + ident('') +
                lparen + delimitedList(ident, ",")('fields') + rparen + index_type('type')
                ).setParseAction(f)

statement = create_graph | create_vertex | \
            create_edge | create_property | \
            create_index


def parse_line(s):
    """
    parses a single line
    :param s:
    :return:
    """
    return statement.parseString(s)[0]


