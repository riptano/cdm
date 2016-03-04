from dse.cluster import Cluster
import readline
import code
import sys

class GraphRepl(code.InteractiveConsole):
    def compile_command(self, code, **kwargs):
        import ipdb; ipdb.set_trace()
        pass



def main():
    session = Cluster().connect()
    session.default_graph_options.graph_name = sys.argv[1]

    while True:
        input = GraphRepl().raw_input("gremlin> ")
        result = session.execute_graph(input)
        for x in result:
            print x

if __name__ == "__main__":
    main()
