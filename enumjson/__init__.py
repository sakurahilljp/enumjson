'''
Iterative JSON parser.

Main API:

- ``enumjson.parse``: iterator returning parsing events with the object tree context,
  see ``enumjson.common.parse`` for docs.

- ``enumjson.items``: iterator returning Python objects found under a specified prefix,
  see ``enumjson.common.items`` for docs.

Top-level ``enumjson`` module exposes method from the pure Python backend. There's
also two other backends using the C library yajl in ``enumjson.backends`` that have
the same API and are faster under CPython.
'''
from enumjson.common import JSONError, IncompleteJSONError, ObjectBuilder
import enumjson.backends.python as backend


__version__ = '2.3'


basic_parse = backend.basic_parse
parse = backend.parse
items = backend.items
