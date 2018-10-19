
import time
import ijson
import json
import enumjson.backends.python as enumjson

def measure(func):
    def wrapper(*args, **kargs):
        start_time = time.time()
        
        result = func(*args, **kargs)
        
        execution_time = time.time() - start_time
        print(f'{func.__name__}: {execution_time}')
        return result
    return wrapper

@measure
def benchmarkenumjson(path):
    with open(path, 'rb') as f:
        x = None
        for item in enumjson.items(f, 'Postal.item'):
           x = json.loads(item)
        #print(type(x), x)

@measure
def benchmarkijson(path):
    with open(path, 'rb') as f:
        x = None
        for item in ijson.items(f, 'Postal.item'):
            x = item
        #print(type(x), x)

@measure
def benchmarkfile(path):
    with open(path, encoding='utf-8') as f:
        for item in f:
            pass

def main(path):
    for _ in range(0, 2):
        benchmarkfile(path)
        benchmarkenumjson(path)
        benchmarkijson(path)
   
if __name__ == "__main__":
    main('var/data.json')
