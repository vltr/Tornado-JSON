# -*- coding: utf-8 -*-

import inspect
import cyclone.web


def asynchronous(func):
    """shissen compatible wrapper for ``cyclone.web.asynchronous``

    Annotates original argspec.args of ``func`` as attribute ``__argspec_args``
    """
    wrapper = cyclone.web.asynchronous(func)
    wrapper.__argspec_args = inspect.getargspec(func).args
    return wrapper
