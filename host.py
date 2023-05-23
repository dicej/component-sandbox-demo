from sandbox import Sandbox
from sandbox.types import Ok, Err
from wasmtime import Config, Engine, Store
import json
import sys
from threading import Timer

TIMEOUT_SECONDS=5

args = sys.argv[1:]
if len(args) == 0:
    print("usage: python3 host.py [<statement>...] <expression>", file=sys.stderr)
    exit(-1)

config = Config()
config.epoch_interruption = True

def on_timeout(engine):
    print("timeout!")
    engine.increment_epoch()

engine = Engine(config)
timer = Timer(TIMEOUT_SECONDS, on_timeout, args=(engine,))
timer.start()

store = Store(engine)
store.set_epoch_deadline(1)

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

timer.cancel()
