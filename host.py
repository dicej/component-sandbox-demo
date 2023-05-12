from sandbox import Sandbox
from sandbox.types import Ok, Err
from wasmtime import Store
import json

def main():
    store = Store()
    sandbox = Sandbox(store)
    result = sandbox.eval('2 + 2')
    if isinstance(result, Ok):
        result = json.loads(result.value)
        print(f"result: {result}")
    else:
        result = result.value
        print(f"error: {result}")
