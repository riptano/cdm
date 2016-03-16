import logging
from collections import namedtuple

from colorama import Fore, Style
from pyparsing import Word, alphas, Keyword, \
                      Optional, LineStart, \
                      alphanums, oneOf, Literal, \
                      CaselessLiteral, OneOrMore, delimitedList

class Noop(Exception): pass
class ParseError(Exception): pass


"""
schema = graph.schema()
def id = schema.buildPropertyKey('id', Integer.class).add()
schema.buildVertexLabel('author').add()
schema.buildEdgeLabel('authored').add()
"""


type_mapping = {
    "int" : "Integer.class",
    "text": "String.class",
}

class ParsedCommand(object):
    result = None
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
        tmp = None
        try:
            self.pre_execute(session)
            print Fore.GREEN + "Command rewritten to:\n{}".format(s) + Style.RESET_ALL
            tmp = session.execute_graph(s)
            self.result = tmp
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


class ShowGraphs(ParsedCommand):
    def to_string(self):
        return "system.graphs"

    def post_execute(self, session):
        print "Available graphs: ",
        i = 0
        for graph in self.result:
            print graph,
            i += 1
            if i % 4 == 0:
                print
        print


class DropGraph(ParsedCommand):
    name = None
    def to_string(self):
        return "system.dropGraph('{}')".format(self.name)


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


"""
 vLabel1.buildVertexIndex('search').search()
.byPropertyKey('p_key_1')
.byPropertyKey('p_key_2', fullTextIndex())
.byPropertyKey('p_key_3', stringIndex())
"""

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


Property = namedtuple("Property", ["name", "type", "cardinality"])
VertexLabel = namedtuple("Label", ["name"])
EdgeLabel = namedtuple("Label", ["name", "cardinality", "directionality"])
VertexIndex = namedtuple("VertexIndex", ["name", "type"])
EdgeIndex = namedtuple("EdgeIndex", ["name", "type"])

class Schema(object):
    objects = {} # dict of lists, { Type: list of elements }
    def add(self, obj):
        # one of the named tuples
        t = type(obj)


class DescribeGraph(ParsedCommand):
    def to_string(self):
        return "graph.schema().traversal().V().valueMap(true)"

    def post_execute(self, session):
        properties = []
        vlabels = []
        elabels = []
        vindex = []
        eindex = []

        for element in self.result:
            element = element.value
            if 'label' not in element:
                continue

            if element['label'] == 'propertyKey':
                properties.append(Property(name=element['name'][0],
                                           type=element['dataType'][0],
                                           cardinality=element['cardinality'][0]))
            elif element['label'] == 'vertexLabel':
                vlabels.append(VertexLabel(name=element['name'][0]))
            elif element['label'] == 'edgeLabel':
                elabels.append(EdgeLabel(name=element['name'][0],
                                         cardinality=element['cardinality'][0],
                                         directionality=element['directionality'][0]))
            elif element['label'] == 'vertexIndex':
                tmp = VertexIndex(name=element['name'][0],
                                  type=element['type'][0])
                vindex.append(tmp)
            # elif element['label'] == 'edgeIndex':
            #     tmp = EdgeIndex(name=element['name'][0],
            #                       type=element['type'][0])

        print "Vertex Labels: ",
        for element in vlabels:
            print element,

        print "\nEdge Labels: ",
        for element in elabels:
            print element,

        print "\nProperties: ",
        for element in elabels:
            print element,

        print "\nVertex Indexes: ",
        for element in vindex:
            print element,


        print "\nEdge Indexes: not implemented "

class UseGraph(ParsedCommand):
    name = None
    def to_string(self):
        return ""

    def pre_execute(self, session):

        if self.name not in session.cluster.metadata.keyspaces:
            print "Graph {}{}{} not found".format(Fore.RED, self.name, Style.RESET_ALL)
        else:
            session.default_graph_options.graph_name = self.name
        raise Noop()

class CreateEdgeIndex(ParsedCommand):
    direction = None
    name = None
    edge = None
    vertex = None
    property = None
    def to_string(self):
        # graph.schema().vertexLabel('reviewer').buildEdgeIndex('ratedByStars', rated).direction(OUT). byPropertyKey('stars').add()
        s = self.schema
        s += "edge_label = schema.edgeLabel('{}')\n".format(self.edge)
        s += "schema.vertexLabel('{vertex}').buildEdgeIndex('{name}', edge_label).direction({direction}).byPropertyKey('{property}').add()".format(vertex=self.vertex, name=self.name, direction=self.direction, property=self.property)
        return s


create = Keyword('create', caseless=True)
property = Keyword('property', caseless=True)
vertex = Keyword('vertex', caseless=True)
edge = Keyword('edge', caseless=True)
graph = Keyword('graph', caseless=True)
graphs = Keyword('graphs', caseless=True)
show = Keyword('show', caseless=True)
drop = Keyword("drop", caseless=True)
index = Keyword('index', caseless=True)
label = Keyword('label', caseless=True)

on_ = Keyword("on", caseless=True).suppress()
use = Keyword('use', caseless=True).suppress()

describe = Keyword("desc", caseless=True) | \
            Keyword("describe", caseless=True)

direction = Keyword("OUT", caseless=True) | Keyword("IN", caseless=True)

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
                setParseAction(lambda s, l, t: CreateGraph(name=t.name))

show_graphs = (show + graphs).setParseAction(lambda s, l, t: ShowGraphs())

use_graph = (use + ident('name')).\
                setParseAction(lambda s, l, t: UseGraph(name=t.name))


create_vertex = (create + vertex + Optional(label) + ident('label')).\
                setParseAction(lambda s, l, t: CreateVertex(label=t.label) )

create_edge = (create + edge + Optional(label) + ident('label')).\
                setParseAction(lambda s, l, t: CreateEdge(label=t.label))

create_property = (create + property + ident("name") + typename("type")).\
                setParseAction(lambda s, l, t: CreateProperty(name=t.name, type=t.type))

drop_graph = (drop + graph + ident('name')).setParseAction(
                lambda s, l, t: DropGraph(name=t.name))

describe_graph = (describe + graph).\
    setParseAction(lambda s, l, t: DescribeGraph())


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


def cei(s, l, t):
    return CreateEdgeIndex(direction=t.direction.upper(),
                           name=t.name,
                           edge=t.edge,
                           vertex=t.vertex,
                           property=t.property)

create_edge_index = (create + direction("direction") + index +
                     ident('name') +
                     on_ + vertex + ident('vertex') +
                     on_ + edge + ident('edge') +
                     lparen + ident('property') + rparen).\
                        setParseAction(cei)


statement = create_graph | use_graph | create_vertex | \
            create_edge | create_property | \
            create_vertex_index | show_graphs | drop_graph |\
            describe_graph | create_edge_index


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


def execute_statements(statements, session):
    """
    executes a list of graph statements, in order, against session
    :param statements:
    :param session:
    :return:
    """
    for s in statements:
        stmt = parse_line(s)
