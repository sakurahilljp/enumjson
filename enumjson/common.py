'''
Backend independent higher level interfaces, common exceptions.
'''


class JSONError(Exception):
    '''
    Base exception for all parsing errors.
    '''
    pass


class IncompleteJSONError(JSONError):
    '''
    Raised when the parser can't read expected data from a stream.
    '''
    pass


def parse(basic_events):
    '''
    An iterator returning parsing events with the information about their location
    with the JSON object tree. Events are tuples ``(prefix, type, value)``.

    Available types and values are:

     ('null', None)
    ('boolean', <True or False>)
    ('number', <int or Decimal>)
    ('string', <unicode>)
    ('map_key', <str>)
    ('start_map', None)
    ('end_map', None)
    ('start_array', None)
    ('end_array', None)

    Prefixes represent the path to the nested elements from the root of the JSON
    document. For example, given this document::

        {
          "array": [1, 2],
          "map": {
            "key": "value"
          }
        }

    the parser would yield events:

      ('', 'start_map', None)
      ('', 'map_key', 'array')
      ('array', 'start_array', None)
      ('array.item', 'number', 1)
      ('array.item', 'number', 2)
      ('array', 'end_array', None)
      ('', 'map_key', 'map')
      ('map', 'start_map', None)
      ('map', 'map_key', 'key')
      ('map.key', 'string', u'value')
      ('map', 'end_map', None)
      ('', 'end_map', None)

    '''
    path = []
    for event, value in basic_events:
        if event == 'map_key':
            prefix = '.'.join(path[:-1])
            path[-1] = value
        elif event == 'start_map':
            prefix = '.'.join(path)
            path.append(None)
        elif event == 'end_map':
            path.pop()
            prefix = '.'.join(path)
        elif event == 'start_array':
            prefix = '.'.join(path)
            path.append('item')
        elif event == 'end_array':
            path.pop()
            prefix = '.'.join(path)
        else:  # any scalar value
            prefix = '.'.join(path)

        yield prefix, event, value


class TextBuilder(object):
    '''
    Incrementally builds an object from JSON parser events. Events are passed
    into the `event` function that accepts two parameters: event type and
    value. The object being built is available at any time from the `value`
    attribute.
    '''

    def __init__(self):
        self.containers = []
        self.keys = []
        c = []
        self.containers.append((c, c.append))

    @property
    def value(self):
        return self.containers[0][0][0]

    def event(self, event, value):
        #print('>>>', event, repr(value))

        if event == 'start_map':
            c = []
            def setter(value):
                #c.append(''.join([self.keys.pop(), ': ', value]))
                c.append(self.keys.pop() + ': ' + value)
            self.containers.append((c, setter))
        elif event == 'start_array':
            c = []
            self.containers.append((c, c.append))
        elif event == 'end_array':
            c, _ = self.containers.pop()
            self.containers[-1][1](''.join(['[', ', '.join(c), ']']))
        elif event == 'end_map':
            c, _ = self.containers.pop()
            self.containers[-1][1](''.join(['{', ', '.join(c), '}']))
        elif event == 'map_key':
            self.keys.append('"' + value + '"')
        elif event == 'string':
            self.containers[-1][1]('"' + value + '"')
        else:
            self.containers[-1][1](value)


def items(prefixed_events, prefix):
    '''
    An iterator returning native Python objects constructed from the events
    under a given prefix.
    '''
    prefixed_events = iter(prefixed_events)
    try:
        while True:
            current, event, value = next(prefixed_events)
            if current == prefix:
                if event in ('start_map', 'start_array'):
                    builder = TextBuilder()
                    end_event = event.replace('start', 'end')
                    while (current, event) != (prefix, end_event):
                        builder.event(event, value)
                        current, event, value = next(prefixed_events)

                    builder.event(event, value)
                    yield builder.value
                else:
                    yield value
    except StopIteration:
        pass
