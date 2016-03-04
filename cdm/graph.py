from dse.cluster import Cluster
import code
import sys


def main():
    session = Cluster().connect()
    session.default_graph_options.graph_name = sys.argv[1]
    accum = None
    eof = None

    while True:
        prompt = "gremlin> " if eof is None else "gremlin (cont)> "

        input = code.InteractiveConsole().raw_input(prompt)
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
        except Exception as e:
            print e
            continue

        for row in result:
            tmp = {}
            for name, val in row.properties.iteritems():
                props = [p['value'] for p in val]
                if len(props) == 1:
                    tmp[name] = props[0]
                else:
                    tmp[name] = props
            print tmp

if __name__ == "__main__":
    main()
