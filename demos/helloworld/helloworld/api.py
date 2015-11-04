# -*- coding: utf-8 -*-

from twisted.internet.defer import maybeDeferred

from shissen.requesthandlers import APIHandler
from shissen import schema
from shissen.async import asynchronous


class HelloWorldHandler(APIHandler):

    # Decorate any HTTP methods with the `schema.validate` decorator
    #   to validate input to it and output from it as per the
    #   the schema ``input_schema`` and ``output_schema`` arguments passed.
    # Simply use `return` rather than `self.write` to write back
    #   your output.
    @schema.validate(
        output_schema={"type": "string"},
        output_example="Hello world!"
    )
    def get(self):
        """Shouts hello to the world!"""
        return "Hello world!"


class PostIt(APIHandler):

    @schema.validate(
        input_schema={
            "type": "object",
            "properties": {
                "title": {"type": "string"},
                "body": {"type": "string"},
                "index": {"type": "number"},
            }
        },
        input_example={
            "title": "Very Important Post-It Note",
            "body": "Equally important message",
            "index": 0
        },
        output_schema={
            "type": "object",
            "properties": {
                "message": {"type": "string"}
            }
        },
        output_example={
            "message": "Very Important Post-It Note was posted."
        },
    )
    def post(self):
        """
        POST the required parameters to post a Post-It note

        * `title`: Title of the note
        * `body`: Body of the note
        * `index`: An easy index with which to find the note
        """
        # `schema.validate` will JSON-decode `self.request.body` for us
        #   and set self.body as the result, so we can use that here
        return {
            "message": "{} was posted.".format(self.body["title"])
        }


class Greeting(APIHandler):

    # When you include extra arguments in the signature of an HTTP
    #   method, Tornado-JSON will generate a route that matches the extra
    #   arguments; here, you can GET /api/greeting/John/Smith and you will
    #   get a response back that says, "Greetings, John Smith!"
    # You can match the regex equivalent of `\w+`.
    @schema.validate(
        output_schema={"type": "string"},
        output_example="Greetings, Named Person!"
    )
    def get(self, fname, lname):
        """Greets you."""
        return "Greetings, {} {}!".format(fname, lname)


class AsyncHelloWorld(APIHandler):

    def hello(self, name):
        return "Hello (asynchronous) world! My name is {}.".format(name)

    @schema.validate(
        output_schema={"type": "string"},
        output_example="Hello (asynchronous) world! My name is Fred."
    )
    # ``shissen.async.asynchronous`` must be used for deferreds
    # ``cyclone.web.asynchronous`` CANNOT be used directly
    @asynchronous
    def get(self, name):
        """Shouts hello to the world (asynchronously)!"""
        # Asynchronously yield a result from a method
        yield maybeDeferred(self.hello, name)


class FreeWilledHandler(APIHandler):

    # And of course, you aren't forced to use schema validation;
    #   if you want your handlers to do something more custom,
    #   they definitely can.
    def get(self):
        # If you don't know where `self.success` comes from, it is defined
        #   in the `JSendMixin` mixin in shissen.jsend. `APIHandler`
        #   inherits from this and thus gets the methods.
        self.success("I don't need no stinkin' schema validation.")
        # If you're feeling really bold, you could even skip JSend
        #   altogether and do the following EVIL thing:
        # self.write("I'm writing back a string that isn't JSON! Take that!")
