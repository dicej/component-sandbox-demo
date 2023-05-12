from sandbox import Sandbox
from sandbox.types import Ok, Err
from wasmtime import Store
import json
import sys

args = sys.argv[1:]
if len(args) == 0:
    print("usage: python3 host.py [<statement>...] <expression>", file=sys.stderr)
    exit(-1)

store = Store()
sandbox = Sandbox(store)
for arg in args[:-1]:
    result = sandbox.exec(store, arg)
    if isinstance(result, Err):
        result = result.value
        print(f"error: {result}")
        exit(-1)

result = sandbox.eval(store, args[-1])
if isinstance(result, Ok):
    result = json.loads(result.value)
    print(f"result: {result}")
else:
    result = result.value
    print(f"error: {result}")
