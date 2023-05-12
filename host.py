from sandbox import Sandbox
from sandbox.types import Ok, Err
from wasmtime import Store
import json
import sys

args = sys.argv[1:]
if len(args) != 1:
    print("please specify an expression to execute in the sandbox", file=sys.stderr)
    exit(-1)

store = Store()
sandbox = Sandbox(store)
result = sandbox.eval(store, args[0])
if isinstance(result, Ok):
    result = json.loads(result.value)
    print(f"result: {result}")
else:
    result = result.value
    print(f"error: {result}")
