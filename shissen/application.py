# -*- coding: utf-8 -*-

import cyclone.web

from shissen.api_doc_gen import api_doc_gen


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

        # if compress_response not in settings:
        #     settings[compress_response] = True
        settings["gzip"] = True

        cyclone.web.Application.__init__(
            self,
            routes,
            **settings
        )
