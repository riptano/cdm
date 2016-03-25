from cdm.installer import Installer, SimpleCQLSchema

class SampleInstaller(Installer, SimpleCQLSchema):
    
    def install_cassandra(self):
        c = self.context

    # def cassandra_schema(self):
    #     return ["CREATE TABLE jon (test int primary key)"]
