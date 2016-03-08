from dse.cluster import Cluster
from dse.graph import SimpleGraphStatement
import code
import sys
from cassandra.cluster import ResultSet
import os
from colorama import Fore, Style, init
import readline
init()
import time
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
        if hasattr(row, 'type'):
            if row.type == "vertex":
                print_vertex(row)
            elif row.type == "edge":
                print "Edge[{}{}{}]".format(Fore.BLUE, row.label, Style.RESET_ALL), row.properties
        else:
            print row.value


def main():
    session = Cluster().connect()
    graph = sys.argv[1]
    session.default_graph_options.graph_name = graph
    accum = None
    eof = None

    print "Gremlin REPL, use heredocs for multiline ex:<<EOF"

    while True:
        prompt = "gremlin> " if eof is None else "gremlin (cont)> "
        input = raw_input(prompt)
        output_time = False
        start_time = time.time()

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

        if input == "%schema":
            continue


        total_time = None
        try:
            stmt = SimpleGraphStatement(input)

            if input.startswith("a"):
                print Fore.GREEN + "Spark Graph Traversal Enabled, this may take a while..." + Style.RESET_ALL
                stmt.options.graph_source = "a"
                stmt.options.graph_alias = "a"
            start = time.time()
            result = session.execute_graph(stmt)
            total_time = time.time() - start

        except Exception as e:
            print e
            continue

        if isinstance(result, ResultSet):
            print_result_set(result)
            if total_time:
                print Fore.RED + "Query Time: {}s".format(round(total_time, 3)) + Style.RESET_ALL
        else:
            try:

                print "Unknown result", type(result), result
            except Exception as e:
                print e


if __name__ == "__main__":
    main()

