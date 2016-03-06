from dse.cluster import Cluster
import code
import sys
import readline
from cassandra.cluster import ResultSet
import os
from colorama import Fore, Style

histfile = os.path.join(os.path.expanduser("~"), ".dsegraphhist")

try:
    readline.read_history_file(histfile)
    # default history len is -1 (infinite), which may grow unruly
    readline.set_history_length(100)
except IOError:
    pass

import atexit
atexit.register(readline.write_history_file, histfile)

def print_vertex(row):
    tmp = {}
    for name, val in row.properties.iteritems():
        props = [p['value'] for p in val]
        if len(props) == 1:
            tmp[name] = props[0]
        else:
            tmp[name] = props
    print "Vertex[{}{}{}]".format(Fore.BLUE, row.label, Style.RESET_ALL), tmp

def print_result_set(result):
    for row in result:
        if row.type == "vertex":
            print_vertex(row)
        elif row.type == "edge":
            print "Edge[{}{}{}]".format(Fore.BLUE, row.label, Style.RESET_ALL), row.properties


def main():
    session = Cluster().connect()
    session.default_graph_options.graph_name = sys.argv[1]
    accum = None
    eof = None

    print "Gremlin REPL, use heredocs for multiline ex:<<EOF"

    while True:
        prompt = "gremlin> " if eof is None else "gremlin (cont)> "
        input = raw_input(prompt)

        if input.startswith("<<"):
            # heredoc
            print "Multiline mode activated"
            eof = input[2:]
            accum = []
            continue

        if eof and input == eof:
            eof = None
            input = "\n".join(accum)
            print input

        elif eof:
            accum.append(input)
            continue

        if input == "quit" or input == "exit":
            break

        try:
            result = session.execute_graph(input)
            # readline.add_history(input)
        except Exception as e:
            print e
            continue

        if isinstance(result, ResultSet):
            print_result_set(result)
        else:
            try:
                print result
            except Exception as e:
                print e


if __name__ == "__main__":
    main()
