import os


def remove_zero_byte_file(search_path):
    target_size = 0
    for dirpath, dirs, files in os.walk(search_path, topdown=False):
        for file in files:
            path = os.path.join(dirpath, file)
            print('%s:%s' % (path, os.stat(path).st_size))
            if os.stat(path).st_size == target_size:
                os.remove(path)



'''
import json
from collections import namedtuple

data = '{"name": "John Smith", "hometown": {"name": "New York", "id": 123}}'

# Parse JSON into an object with attributes corresponding to dict keys.
x = json.loads(data, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
print x.name, x.hometown.name, x.hometown.id
or, to reuse this easily:

def _json_object_hook(d): return namedtuple('X', d.keys())(*d.values())
def json2obj(data): return json.loads(data, object_hook=_json_object_hook)

x = json2obj(data)


'''