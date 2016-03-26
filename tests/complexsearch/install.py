from cdm.installer import Installer, SimpleCQLSchema

class SearchInstaller(SimpleCQLSchema, Installer):

    def install_cassandra(self):
        c = self.context

