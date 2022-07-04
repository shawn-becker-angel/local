# file: file-info.py_compile

from collections import namedtuple
from typing import NamedTuple


__all__ = ['FileInfo']

class FileInfo(NamedTuple):
    path: str = '' # absolute path to a file
    bytes: int = 0  # filesize in bytes