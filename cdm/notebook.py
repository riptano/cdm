"""
notebook extension for all magic we need for tutorials
"""
from IPython.core.magic import Magics, magics_class, cell_magic, line_magic, needs_local_scope


@magics_class
class CDMMagic(Magics):
    pass



def load_ipython_extension(ipython):
    # set up the session and the spark context
    ipython.register_magics(CDMMagic)

