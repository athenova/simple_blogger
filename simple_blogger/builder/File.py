from dataclasses import dataclass
from io import IOBase

@dataclass
class File:
    ext: str
    file: IOBase