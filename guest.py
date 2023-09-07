import sandbox
from sandbox.types import Err
import json
import numpy

class Sandbox(sandbox.Sandbox):
    def eval(self, expression: str) -> str:
        try:
            return json.dumps(eval(expression))
        except Exception as e:
            raise_err(e)

    def exec(self, statements: str):
        try:
            exec(statements)
        except Exception as e:
            raise_err(e)
            
def raise_err(e: Exception):
    message = str(e)
    if message == '':
        raise Err(f"{type(e).__name__}")
    else:
        raise Err(f"{type(e).__name__}: {message}")
