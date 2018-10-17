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
      "false": false,
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

class TestYajl2Bakend(unittest.TestCase):

    def test_basic_parse(self):
        for item in basic_parse(BytesIO(JSON)):
            print(item)

    def test_parse(self):
        for item in parse(basic_parse(BytesIO(JSON))):
            print(item)



if __name__ == "__main__":
    unittest.main()