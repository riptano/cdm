from collections import namedtuple

from pyparsing import Word, alphas, Keyword, Optional, LineStart, \
                    alphanums, oneOf, Literal, CaselessLiteral, OneOrMore, delimitedList

class Noop(Exception): pass
class ParseError(Exception): pass

"""
schema = graph.schema()
def id = schema.buildPropertyKey('id', Integer.class).add()
schema.buildVertexLabel('author').add()
schema.buildEdgeLabel('authored').add()
"""

import logging

type_mapping = {
    "int" : "Integer.class",
    "text": "String.class",
}

class ParsedCommand(object):

    def __init__(self, **kwargs):
        for k, v in kwargs.iteritems():
            self.__setattr__(k, v)

    def to_string(self):
        raise NotImplementedError()

    def __str__(self):
        return self.to_string()

    # don't mess with this on a subclass, look at pre_execute and post_execute
    def execute(self, session):
        s = str(self)
        logging.info(s)
        print s
        tmp = None
        try:
            self.pre_execute(session)
            print "Command rewritten to {}".format(s)
            tmp = session.execute_graph(s)
        except Noop:
            pass

        self.post_execute(session)
        return tmp

    def pre_execute(self, session):
        pass

    def post_execute(self, session):
        pass

    @property
    def schema(self):
        return "schema = graph.schema()\n"


# schema.buildVertexLabel('author').add()
class CreateVertex(ParsedCommand):
    label = None
    def to_string(self):
        return self.schema + "schema.buildVertexLabel('{}').add()".format(self.label)


class CreateEdge(ParsedCommand):
    label = None
    def to_string(self):
        tmp = self.schema + "schema.buildEdgeLabel('{}').add()".format(self.label)
        return tmp


# def id = schema.buildPropertyKey('id', Integer.class).add()
class CreateProperty(ParsedCommand):
    name = None
    type = None
    def to_string(self):
        t = self.type.lower()
        if t in type_mapping:
            t = type_mapping[t]

        return self.schema + "schema.buildPropertyKey('{}', {}).add()".format(self.name, t)


class CreateVertexIndex(ParsedCommand):
    label = None
    name = None
    fields = None
    type = None

    def to_string(self):
        s = """graph.schema().vertexLabel("{}").buildVertexIndex("{}").{}().byPropertyKey("{}").add()""".format(self.label, self.name, self.type, self.fields[0])
        return s


class CreateGraph(ParsedCommand):
    name = None
    def to_string(self):
        return """system.createGraph('{}').build()""".format(self.name)

    def pre_execute(self, session):
        self.old_name = session.default_graph_options.graph_name
        session.default_graph_options.graph_name = None

    def post_execute(self, session):
        print "{} graph created".format(self.name)
        session.default_graph_options.graph_name = self.old_name

    def execute(self, session):
        super(CreateGraph, self).execute(session)



class UseGraph(ParsedCommand):
    name = None
    def to_string(self):
        return ""

    def pre_execute(self, session):
        session.default_graph_options.graph_name = self.name
        raise Noop()

create = Keyword('create', caseless=True)
property = Keyword('property', caseless=True)
vertex = Keyword('vertex', caseless=True)
edge = Keyword('edge', caseless=True)
graph = Keyword('graph', caseless=True)

index = Keyword('index', caseless=True)
label = Keyword('label', caseless=True)

on_ = Keyword("on", caseless=True).suppress()
use = Keyword('use', caseless=True).suppress()

# index types
materialized = Keyword("materialized", caseless=True)
fulltext = Keyword("search", caseless=True)
secondary = Keyword("secondary", caseless=True)

index_type = materialized | fulltext | secondary

lparen = Literal("(").suppress()
rparen = Literal(")").suppress()

ident =  Word(alphas, alphanums + "_")

typename = oneOf("""ascii bigint blob boolean counter date
                  decimal double float inet int smallint text time
                  timestamp timeuuid tinyint uuid varchar varint""", caseless=True)

create_graph = (create + graph + ident('name')).\
                setParseAction(lambda s,l,t: CreateGraph(name=t.name))

use_graph = (use + ident('name')).\
                setParseAction(lambda s,l,t: UseGraph(name=t.name))


create_vertex = (create + vertex + Optional(label) + ident('label')).\
                setParseAction(lambda s, l, t: CreateVertex(label=t.label) )

create_edge = (create + edge + Optional(label) + ident('label')).\
                setParseAction(lambda s, l, t: CreateEdge(label=t.label))

create_property = (create + property + ident("name") + typename("type")).\
                setParseAction(lambda s, l, t: CreateProperty(name=t.name, type=t.type))

def vi(s,l,t):
    return CreateVertexIndex(label=t.label,
                             name=t.index_name,
                             fields=t.fields,
                             type=t.type)


create_vertex_index = (create + index_type('type') + index + \
                        ident('index_name') +
                        on_ + vertex.suppress() + ident('label') +
                        lparen + delimitedList(ident, ",")('fields') + rparen).\
                       setParseAction(vi)

statement = create_graph | use_graph | \
            create_vertex | \
            create_edge | create_property | \
            create_vertex_index


def parse_line(s):
    """
    parses a single line
    :param s:
    :return:
    """
    try:
        return statement.parseString(s)[0]
    except:
        raise ParseError()


