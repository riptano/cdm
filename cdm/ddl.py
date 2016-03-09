from pyparsing import Word, alphas, Keyword, Optional, LineStart, alphanums

create = Keyword('create', caseless=True)
property = Keyword('property', caseless=True)
vertex = Keyword('vertex', caseless=True)
edge = Keyword('edge', caseless=True)

index = Keyword('index', caseless=True)

ident = alphas + Word(alphas, alphanums + "_")



def parse_line(s):
    """
    parses a single line
    :param s:
    :return:
    """


