# -*- coding: utf-8 -*-

from shissen.requesthandlers import APIHandler


DATA = {
    "Ford": {
        "Fusion": {
            "2013": "http://www.ford.ca/cars/fusion/2013/",
            "2014": "http://www.ford.ca/cars/fusion/2014/"
        },
        "Taurus": {
            "2013": "http://www.ford.ca/cars/taurus/2013/",
            "2014": "http://www.ford.ca/cars/taurus/2014/"
        }
    }
}


class CarsAPIHandler(APIHandler):

    # APIHandler has two "special" attributes:
    #   * __url_names__ :
    #       This is a list of names you'd like the
    #       the requesthandler to be called in auto-
    #       generated routes, i.e., since the absolute
    #       path of this handler (in context of the
    #       ``cars`` package) is, ``cars.api.CarsAPIHandler``,
    #       if you've read earlier documentation, you'll
    #       know that the associated URL to this that
    #       will be autogenerated is "/api/carsapi".
    #       __url_names__ can change the last ``carsapi``
    #       part to whatever is in the list. So in this
    #       case, we change it to "/api/cars". If we added
    #       additional names to the list, we would generate
    #       more routes with the given names.
    #       Of course, this isn't an actual handler, just
    #       a handy superclass that we'll let all of the handlers
    #       below inherit from so they can have a base URL of
    #       "/api/cars" also, but extended to match additional
    #       things based on the parameters of their ``get`` methods.
    #
    #       An important note on __url_names__ is that by default,
    #       it exists as ``__url_names__ = ["__self__"]``. The
    #       ``__self__`` is a special value, which means that the
    #       requesthandler should get a URL such as the ones you
    #       assigned to the handlers in the Hello World demo.
    #       You can either ADD to the list to keep this, or
    #       create a new list to not.
    #
    #   * __urls__ :
    #       I'll mention __urls__ as well; this let's you just
    #       assign a completely custom URL pattern to match to
    #       the requesthandlers, i.e., I could add something like,
    #           ``__urls__ = [r"/api/cars/?"]``
    #       and that would give me the exact same URL mapped
    #       to this handler, but defined by me. Note that both
    #       URLs generated from ``__url_names__`` and URLs provided
    #       by you in ``__urls__`` will be created and assigned to
    #       the associated requesthandler, so make sure to modify/overwrite
    #       both attributes to get only the URLs mapped that you want.
    #
    __url_names__ = ["cars"]


class MakeListHandler(CarsAPIHandler):

    def get(self):
        self.success(DATA.keys())


class MakeHandler(CarsAPIHandler):

    def get(self, make):
        try:
            self.success(DATA[make])
        except KeyError:
            self.fail("No data on such make `{}`.".format(make))


class ModelHandler(CarsAPIHandler):

    def get(self, make, model):
        try:
            self.success(DATA[make][model])
        except KeyError:
            self.fail("No data on `{} {}`.".format(make, model))


class YearHandler(CarsAPIHandler):

    def get(self, make, model, year):
        try:
            self.success(DATA[make][model][year])
        except KeyError:
            self.fail("No data on `{} {} {}`.".format(year, make, model))


# Routes for the handlers above will look like this:
#
# [
#   [
#     "/api/cars/?",
#     "<class 'cars.api.MakeListHandler'>"
#   ],
#   [
#     "/api/cars/(?P<make>[a-zA-Z0-9_\-]+)/(?P<model>[a-zA-Z0-9_\-]+)/?$",
#     "<class 'cars.api.ModelHandler'>"
#   ],
#   [
#     "/api/cars/(?P<make>[a-zA-Z0-9_\-]+)/(?P<model>[a-zA-Z0-9_\-]+)/(?P<year>[a-zA-Z0-9_\-]+)/?$",
#     "<class 'cars.api.YearHandler'>"
#   ],
#   [
#     "/api/cars/(?P<make>[a-zA-Z0-9_\-]+)/?$",
#     "<class 'cars.api.MakeHandler'>"
#   ]
# ]
