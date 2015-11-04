# -*- coding: utf-8 -*-

from cyclone.web import RequestHandler
from twisted.python.failure import Failure
from jsonschema import ValidationError

from shissen.jsend import JSendMixin
from shissen.exceptions import APIError


class BaseHandler(RequestHandler):
    """BaseHandler for all other RequestHandlers"""

    __url_names__ = ["__self__"]
    __urls__ = []


class APIHandler(BaseHandler, JSendMixin):
    """RequestHandler for API calls

    - Sets header as ``application/json``
    - Provides custom write_error that writes error back as JSON \
    rather than as the standard HTML template
    """

    def initialize(self):
        """
        - Set Content-type for JSON
        """
        self.set_header("Content-Type", "application/json")

    def write_error(self, status_code, **kwargs):
        """Override of RequestHandler.write_error

        Calls ``error()`` or ``fail()`` from JSendMixin depending on which
        exception was raised with provided reason and status code.

        :type  status_code: int
        :param status_code: HTTP status code
        """
        def get_exc_message(exception):
            return exception.log_message if \
                hasattr(exception, "log_message") else str(exception)

        self.clear()
        self.set_status(status_code)

        # Any APIError exceptions raised will result in a JSend fail written
        # back with the log_message as data. Hence, log_message should NEVER
        # expose internals. Since log_message is proprietary to HTTPError
        # class exceptions, all exceptions without it will return their
        # __str__ representation.
        # All other exceptions result in a JSend error being written back,
        # with log_message only written if debug mode is enabled
        exception = kwargs["exception"]
        if isinstance(exception, Failure):
            exception = exception.value

        if any(isinstance(exception, c) for c in [APIError, ValidationError]):
            # ValidationError is always due to a malformed request
            if isinstance(exception, ValidationError):
                self.set_status(400)
            self.fail(get_exc_message(exception))
        else:
            self.error(
                message=self._reason,
                data=get_exc_message(exception) if self.settings.get("debug")
                else None,
                code=status_code
            )
