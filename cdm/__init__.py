from cdm.context import Context
from cdm.util import get_session
import os
import os.path


def install_local(dataset, main):
    """
    :param dataset:
    :param main:
    :return:
    """

    if not os.path.exists("cache"):
        os.mkdir("cache")

    # apply schema change

    c = Context(dataset=dataset,
                session=get_session(dataset),
                cache_dir="cache")

    # c.clean_cache()
    main(c)
