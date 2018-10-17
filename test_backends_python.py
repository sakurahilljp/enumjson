import unittest
from io import BytesIO, StringIO
from enumjson.backends.python import basic_parse
from enumjson.common import parse

JSON = b'''
{
  "docs": [
    {
      "null": null,
      "boolean": false,
      "true": true,
      "integer": 0,
      "double": 0.5,
      "exponent": 1.0e+2,
      "long": 10000000000,
      "string": "\\u0441\\u0442\\u0440\\u043e\\u043a\\u0430 - \xd1\x82\xd0\xb5\xd1\x81\xd1\x82"
    },
    {
      "meta": [[1], {}]
    },
    {
      "meta": {"key": "value"}
    },
    {
      "meta": null
    }
  ]
}
'''

JSON_EVENTS = [
    ('start_map', None),
    ('map_key', 'docs'),
    ('start_array', None),
    ('start_map', None),
    ('map_key', 'null'),
    ('null', 'null'),
    ('map_key', 'boolean'),
    ('boolean', 'false'),
    ('map_key', 'true'),
    ('boolean', 'true'),
    ('map_key', 'integer'),
    ('number', '0'),
    ('map_key', 'double'),
    ('number', '0.5'),
    ('map_key', 'exponent'),
    ('number', '1.0e+2'),
    ('map_key', 'long'),
    ('number', '10000000000'),
    ('map_key', 'string'),
    ('string', 'строка - тест'),
    ('end_map', None),
    ('start_map', None),
    ('map_key', 'meta'),
    ('start_array', None),
    ('start_array', None),
    ('number', '1'),
    ('end_array', None),
    ('start_map', None),
    ('end_map', None),
    ('end_array', None),
    ('end_map', None),
    ('start_map', None),
    ('map_key', 'meta'),
    ('start_map', None),
    ('map_key', 'key'),
    ('string', 'value'),
    ('end_map', None),
    ('end_map', None),
    ('start_map', None),
    ('map_key', 'meta'),
    ('null', 'null'),
    ('end_map', None),
    ('end_array', None),
    ('end_map', None),
]


class TestPythonBakend(unittest.TestCase):

    def test_basic_parse(self):
        events = list(basic_parse(BytesIO(JSON)))
        for item in events:
            print(item)

        self.assertEqual(events, JSON_EVENTS)
      
    def test_parse(self):
        for item in parse(basic_parse(BytesIO(JSON))):
            print(item)


if __name__ == "__main__":
    unittest.main()
