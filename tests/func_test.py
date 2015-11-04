# -*- coding: utf-8 -*-

import sys
import json

import cyclone.testing
import cyclone.httpclient

from .utils import handle_import_error

try:
    sys.path.append('.')
    from shissen import routes
    from shissen import schema
    from shissen import application
    from shissen import requesthandlers
    sys.path.append('demos/helloworld')
    import helloworld
except ImportError as err:
    handle_import_error(err)


def jd(obj):
    return json.dumps(obj)


def jl(s):
    return json.loads(s.decode("utf-8"))


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
        ]
        return application.Application(
            routes=rts,
            settings={"debug": True},
        )

    def test_synchronous_handler(self):
        def _cb(r):
            self.assertEqual(r.get_status(), 200)
            self.assertEqual(
                jl(r.content)["data"],
                "Hello world!"
            )
        d = self.client.get(
            "/api/helloworld"
        )
        d.addCallback(_cb)
        return d

    def test_asynchronous_handler(self):
        def _cb(r):
            self.assertEqual(r.get_status(), 200)
            self.assertEqual(
                jl(r.content)["data"],
                "Hello (asynchronous) world! My name is name."
            )
        d = self.client.get(
            "/api/asynchelloworld/name"
        )
        d.addCallback(_cb)
        return d

    def test_post_request(self):
        def _cb(r):
            self.assertEqual(r.get_status(), 200)
            self.assertEqual(
                jl(r.content)["data"]["message"],
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
        return d

    def test_url_pattern_route(self):
        def _cb(r):
            self.assertEqual(r.get_status(), 200)
            self.assertEqual(
                jl(r.content)["data"],
                "Greetings, John Smith!"
            )
        d = self.client.get(
            "/api/greeting/John/Smith"
        )
        d.addCallback(_cb)
        return d

    def test_malformed_output(self):
        # Test malformed output
        def _cb(r):
            self.assertEqual(r.get_status(), 500)
            self.assertEqual(
                jl(r.content)["status"],
                "error"
            )
        d = self.client.get(
            "/api/explodinghandler"
        )
        d.addCallback(_cb)
        return d

    def test_malformed_input(self):
        # Test malformed input
        def _cb(r):
            self.assertEqual(r.get_status(), 400)
            self.assertEqual(
                jl(r.content)["status"],
                "fail"
            )
        d = self.client.post(
            "/api/explodinghandler",
            # method="POST",
            body='"Yup", "this is going to end badly."]'
        )
        d.addCallback(_cb)
        return d

    def test_empty_output(self):
        # Test empty output
        def _cb(r):
            self.assertEqual(r.get_status(), 404)
            self.assertEqual(
                jl(r.content)["status"],
                "fail"
            )
        d = self.client.get(
            "/api/notfoundhandler"
        )
        d.addCallback(_cb)
        return d

    def test_empty_output_on_empty_404(self):
        # Test empty output on_empty_404 is False
        def _cb(r):
            self.assertEqual(r.get_status(), 500)
            self.assertEqual(
                jl(r.content)["status"],
                "error"
            )
        d = self.client.post(
            "/api/notfoundhandler",
            # method="POST",
            body="1"
        )
        d.addCallback(_cb)
        return d
