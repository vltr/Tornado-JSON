#!/usr/bin/env python2.7

# ---- The following so demo can be run without having to install package ----#
import sys
import json

from twisted.internet import reactor
sys.path.append("../../")
# ---- Can be removed if Tornado-JSON is installed ----#
# This module contains essentially the same boilerplate
#   as the corresponding one in the helloworld example;
#   refer to that for details.
from tornado_json.routes import get_routes
from tornado_json.application import Application


def main():
    import cars
    routes = get_routes(cars)
    print("Routes\n======\n\n" + json.dumps(
        [(url, repr(rh)) for url, rh in routes],
        indent=2)
    )
    application = Application(routes=routes, settings={})
    reactor.listenTCP(8888, application)
    reactor.run()


if __name__ == '__main__':
    main()
