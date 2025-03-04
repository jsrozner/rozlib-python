import logging
import sys
from typing import Any


class Tee:
    orig_pipe: Any

    def flush(self):
        self.orig_pipe.flush()

class TeeErr(Tee):
    def __init__(self):
        super().__init__()
        self.orig_pipe = sys.stderr

        sys.stderr = self

    def write(self, data):
        if data.strip() == "":
            return
        # todo: I am surprised that logging.error calls do not directly get routed here
        logging.error(f"err: {data}")

    def __del__(self):
        sys.stderr = self.orig_pipe

class TeeOut(Tee):
    def __init__(self):
        super().__init__()
        self.orig_pipe = sys.stdout

        sys.stdout = self

    def write(self, data):
        if data.strip() == "":
            return
        logging.info(f"print: {data}")


    def __del__(self):
        sys.stdout = self.orig_pipe