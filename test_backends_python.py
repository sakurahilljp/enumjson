import unittest
from io import BytesIO, StringIO
import enumjson.backends
from enumjson.common import parse
from enumjson.common import items

from enumjson.common import TextBuilder

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
      "meta": [[1, 2], {}]
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
    ('number', '2'),
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

JSON_TAG_EVENTS = [
    ('', 'start_map', None),
    ('', 'map_key', 'docs'),
    ('docs', 'start_array', None),
    ('docs.item', 'start_map', None),
    ('docs.item', 'map_key', 'null'),
    ('docs.item.null', 'null', 'null'),
    ('docs.item', 'map_key', 'boolean'),
    ('docs.item.boolean', 'boolean', 'false'),
    ('docs.item', 'map_key', 'true'),
    ('docs.item.true', 'boolean', 'true'),
    ('docs.item', 'map_key', 'integer'),
    ('docs.item.integer', 'number', '0'),
    ('docs.item', 'map_key', 'double'),
    ('docs.item.double', 'number', '0.5'),
    ('docs.item', 'map_key', 'exponent'),
    ('docs.item.exponent', 'number', '1.0e+2'),
    ('docs.item', 'map_key', 'long'),
    ('docs.item.long', 'number', '10000000000'),
    ('docs.item', 'map_key', 'string'),
    ('docs.item.string', 'string', 'строка - тест'),
    ('docs.item', 'end_map', None),
    ('docs.item', 'start_map', None),
    ('docs.item', 'map_key', 'meta'),
    ('docs.item.meta', 'start_array', None),
    ('docs.item.meta.item', 'start_array', None),
    ('docs.item.meta.item.item', 'number', '1'),
    ('docs.item.meta.item.item', 'number', '2'),
    ('docs.item.meta.item', 'end_array', None),
    ('docs.item.meta.item', 'start_map', None),
    ('docs.item.meta.item', 'end_map', None),
    ('docs.item.meta', 'end_array', None),
    ('docs.item', 'end_map', None),
    ('docs.item', 'start_map', None),
    ('docs.item', 'map_key', 'meta'),
    ('docs.item.meta', 'start_map', None),
    ('docs.item.meta', 'map_key', 'key'),
    ('docs.item.meta.key', 'string', 'value'),
    ('docs.item.meta', 'end_map', None),
    ('docs.item', 'end_map', None),
    ('docs.item', 'start_map', None),
    ('docs.item', 'map_key', 'meta'),
    ('docs.item.meta', 'null', 'null'),
    ('docs.item', 'end_map', None),
    ('docs', 'end_array', None),
    ('', 'end_map', None),
]


class TestPythonBakend(unittest.TestCase):
    backend = enumjson.backends.python

    def test_basic_parse(self):
        events = list(self.backend.basic_parse(BytesIO(JSON)))
        builder = TextBuilder()
        for item in events:
            # print(item)
            builder.event(*item)

        self.assertEqual(events, JSON_EVENTS)

        # print(builder.value)
        events = list(self.backend.basic_parse(
            BytesIO(builder.value.encode('utf-8'))))
        self.assertEqual(events, JSON_EVENTS)

    def test_parse(self):
        tags = list(parse(self.backend.basic_parse(BytesIO(JSON))))
        self.assertEqual(tags, JSON_TAG_EVENTS)

    def test_items(self):
        events = list(self.backend.basic_parse(BytesIO(JSON)))
        meta = list(items(parse(events), 'docs.item.meta'))
        self.assertEqual(meta, ['[[1, 2], {}]', '{"key": "value"}', 'null'])


if __name__ == "__main__":
    unittest.main()
