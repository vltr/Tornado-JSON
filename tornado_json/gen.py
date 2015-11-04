# -*- coding: utf-8 -*-

import inspect
import cyclone.web


def coroutine(func):
    """Tornado-JSON compatible wrapper for ``tornado.gen.coroutine``

    Annotates original argspec.args of ``func`` as attribute ``__argspec_args``
    """
    wrapper = cyclone.web.asynchronous(func)
    wrapper.__argspec_args = inspect.getargspec(func).args
    return wrapper
