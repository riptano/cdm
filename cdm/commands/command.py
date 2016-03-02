class Command(object):
    subcommand = None

    def __init__(self):
        if self.command is None:
            raise NotImplementedError("implementing the subcommand is required")
