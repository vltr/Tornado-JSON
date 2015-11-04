# -*- coding: utf-8 -*-

import sys
from traceback import print_exc


def handle_import_error(err):  # pragma: no cover
    print_exc()
    print("Please run `py.test` from the root project directory")
    sys.exit(1)
