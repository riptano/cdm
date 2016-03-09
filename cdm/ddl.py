from pyparsing import Word, alphas, Keyword, Optional, LineStart, alphanums

create = Keyword('create', caseless=True)
property = Keyword('property', caseless=True)
vertex = Keyword('vertex', caseless=True)
edge = Keyword('edge', caseless=True)

index = Keyword('index', caseless=True)
label = Keyword('label', caseless=True)
on_ = Keyword("on", caseless=True)

ident =  Word(alphas, alphanums + "_")

create_vertex = create + vertex + Optional(label) + ident('label')


class CreateVertex(object):
    label = None

    def __init__(self, label):
        self.label = label


class CreateEdge(object):
    label = None

    def __init__(self, label):
        self.label = label


def parse_line(s):
    """
    parses a single line
    :param s:
    :return:
    """


