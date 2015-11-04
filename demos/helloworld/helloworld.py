#!/usr/bin/env python2.7

import sys
import json

from twisted.internet import reactor
from twisted.python import log
# ---- The following so demo can be run without having to install package ----#
sys.path.append("../../")
# ---- Can be removed if Tornado-JSON is installed ----#
from tornado_json.routes import get_routes
from tornado_json.application import Application


def main():
    # Pass the web app's package the get_routes and it will generate
    #   routes based on the submodule names and ending with lowercase
    #   request handler name (with 'handler' removed from the end of the
    #   name if it is the name).
    # [("/api/helloworld", helloworld.api.HelloWorldHandler)]
    import helloworld
    routes = get_routes(helloworld)
    print("Routes\n======\n\n" + json.dumps(
        [(url, repr(rh)) for url, rh in routes],
        indent=2)
    )
    log.startLogging(sys.stdout)
    # Create the application by passing routes and any settings
    application = Application(routes=routes, settings={})

    # Start the application on port 8888
    reactor.listenTCP(8888, application)
    reactor.run()


if __name__ == '__main__':
    main()
