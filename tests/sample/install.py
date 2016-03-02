from cdm.installer import Installer

class SampleInstaller(Installer):
    def install_cassandra(self):
        c = self.context
