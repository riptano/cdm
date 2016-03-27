from cdm.installer import Installer, SimpleCQLSchema, AutoGenerateSolrResources

class SearchInstaller(SimpleCQLSchema, Installer):

    def install_cassandra(self):
        c = self.context

    def search_schema(self):
        return [AutoGenerateSolrResources(table="movies")]
