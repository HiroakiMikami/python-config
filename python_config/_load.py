from typing import IO

from python_config._parse import parse


def load(f: IO):
    return parse(f.read())
