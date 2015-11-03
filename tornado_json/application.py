# -*- coding: utf-8 -*-

import cyclone.web

from tornado_json.api_doc_gen import api_doc_gen
# from tornado_json.constants import TORNADO_MAJOR


class Application(cyclone.web.Application):
    """Entry-point for the app

    - Generate API documentation using provided routes
    - Initialize the application

    :type  routes: [(url, RequestHandler), ...]
    :param routes: List of routes for the app
    :type  settings: dict
    :param settings: Settings for the app
    :param  db_conn: Database connection
    """

    def __init__(self, routes, settings):
        # Generate API Documentation
        api_doc_gen(routes)

        # Unless compress_response was specifically set to False in
        # settings, enable it
        # compress_response = "compress_response" if TORNADO_MAJOR >= 4 else "gzip"
        # if compress_response not in settings:
        #     settings[compress_response] = True
        settings["gzip"] = True

        cyclone.web.Application.__init__(
            self,
            routes,
            **settings
        )
