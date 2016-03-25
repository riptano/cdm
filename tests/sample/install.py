from cdm.installer import Installer, SimpleCQLSchema

class SampleInstaller(SimpleCQLSchema, Installer):

    def install_cassandra(self):
        c = self.context

