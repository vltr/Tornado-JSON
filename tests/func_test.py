# -*- coding: utf-8 -*-

import sys
import json

# from tornado.testing import AsyncHTTPTestCase
# from cyclone.testing import CycloneTestCase
import cyclone.testing
import cyclone.httpclient
from twisted.internet import defer
from twisted.internet.defer import returnValue

from .utils import handle_import_error

try:
    sys.path.append('.')
    from tornado_json import routes
    from tornado_json import schema
    from tornado_json import application
    from tornado_json import requesthandlers
    sys.path.append('demos/helloworld')
    import helloworld
except ImportError as err:
    handle_import_error(err)


def jd(obj):
    return json.dumps(obj)


def jl(s):
    return json.loads(s.decode("utf-8"))


# class DummyView(requesthandlers.ViewHandler):
#     """Dummy ViewHandler for coverage"""
#     def delete(self):
#         # Reference db_conn to test for AttributeError
#         self.db_conn


# class DBTestHandler(requesthandlers.APIHandler):
#     """APIHandler for testing db_conn"""
#     def get(self):
#         # Set application.db_conn to test if db_conn BaseHandler
#         #   property works
#         self.application.db_conn = {"data": "Nothing to see here."}
#         self.success(self.db_conn.get("data"))


class ExplodingHandler(requesthandlers.APIHandler):

    @schema.validate(**{
        "input_schema": None,
        "output_schema": {
            "type": "number",
        }
    })
    def get(self):
        """This handler is used for testing purposes and is explosive."""
        return "I am not the handler you are looking for."

    @schema.validate(**{
        "input_schema": {
            "type": "number",
        },
        "output_schema": {
            "type": "number",
        }
    })
    def post(self):
        """This handler is used for testing purposes and is explosive."""
        return "Fission mailed."


class NotFoundHandler(requesthandlers.APIHandler):

    @schema.validate(**{
        "output_schema": {
            "type": "number",
        },
        "on_empty_404": True
    })
    def get(self):
        """This handler is used for testing empty output."""
        return 0

    @schema.validate(**{
        "input_schema": {
            "type": "number",
        },
        "output_schema": {
            "type": "object",
            "properties": {
                "name": {"type": "string"}
            },
            "required": ["name", ]
        }
    })
    def post(self):
        """This handler is used for testing empty json output."""
        return {}


class APIFunctionalTest(cyclone.testing.CycloneTestCase):

    def app_builder(self):
        rts = routes.get_routes(helloworld)
        rts += [
            ("/api/explodinghandler", ExplodingHandler),
            ("/api/notfoundhandler", NotFoundHandler),
            # ("/views/someview", DummyView),
            # ("/api/dbtest", DBTestHandler)
        ]
        return application.Application(
            routes=rts,
            settings={"debug": True},
        )

    def test_synchronous_handler(self):
        def _cb(r):
            self.assertEqual(r.code, 200)
            self.assertEqual(
                jl(r.body)["data"],
                "Hello world!"
            )
        d = self.client.get(
            "/api/helloworld"
        )
        d.addCallback(_cb)

    def test_asynchronous_handler(self):
        def _cb(r):
            self.assertEqual(r.code, 200)
            self.assertEqual(
                jl(r.body)["data"],
                "Hello (asynchronous) world! My name is name."
            )
        d = self.client.get(
            "/api/asynchelloworld/name"
        )
        d.addCallback(_cb)

    def test_post_request(self):
        def _cb(r):
            self.assertEqual(r.code, 200)
            self.assertEqual(
                jl(r.body)["data"]["message"],
                "Very Important Post-It Note was posted."
            )

        d = self.client.post(
            "/api/postit",
            # method="POST",
            body=jd({
                "title": "Very Important Post-It Note",
                "body": "Equally important message",
                "index": 0
            })
        )
        d.addCallback(_cb)

    def test_url_pattern_route(self):
        def _cb(r):
            self.assertEqual(r.code, 200)
            self.assertEqual(
                jl(r.body)["data"],
                "Greetings, John Smith!"
            )
        d = self.client.get(
            "/api/greeting/John/Smith"
        )
        d.addCallback(_cb)

    def test_write_error(self):
        # Test malformed output
        def _cb1(r):
            self.assertEqual(r.code, 500)
            self.assertEqual(
                jl(r.body)["status"],
                "error"
            )
        d1 = self.client.get(
            "/api/explodinghandler"
        )
        d1.addCallback(_cb1)

        # Test malformed input
        def _cb2(r):
            self.assertEqual(r.code, 400)
            self.assertEqual(
                jl(r.body)["status"],
                "fail"
            )
        d2 = self.client.post(
            "/api/explodinghandler",
            # method="POST",
            body='"Yup", "this is going to end badly."]'
        )
        d2.addCallback(_cb2)

    def test_empty_resource(self):
        # Test empty output
        def _cb1(r):
            self.assertEqual(r.code, 404)
            self.assertEqual(
                jl(r.body)["status"],
                "fail"
            )
        d1 = self.client.get(
            "/api/notfoundhandler"
        )
        d1.addCallback(_cb1)

        # Test empty output on_empty_404 is False
        def _cb2(r):
            self.assertEqual(r.code, 500)
            self.assertEqual(
                jl(r.body)["status"],
                "error"
            )
        d2 = self.client.post(
            "/api/notfoundhandler",
            # method="POST",
            body="1"
        )
        d2.addCallback(_cb2)

    # def test_view_db_conn(self):
    #     r = self.fetch(
    #         "/views/someview",
    #         method="DELETE"
    #     )
    #     self.assertEqual(r.code, 500)
    #     self.assertTrue(
    #         "No database connection was provided." in r.body.decode("UTF-8")
    #     )

    # def test_db_conn(self):
    #     r = self.fetch(
    #         "/api/dbtest",
    #         method="GET"
    #     )
    #     self.assertEqual(r.code, 200)
    #     print(r.body)
    #     self.assertEqual(
    #         jl(r.body)["status"],
    #         "success"
    #     )
    #     self.assertTrue(
    #         "Nothing to see here." in jl(r.body)["data"]
    #     )
