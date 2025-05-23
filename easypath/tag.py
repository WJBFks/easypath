import pathlib
from typing_extensions import NamedTuple
from .core import EasyPath, PosixEasyPath, WindowsEasyPath


class EasyPathEasyPath(PosixEasyPath, WindowsEasyPath):
    def __del__(self):
        pass

    def __rtruediv__(self, other):
        return EasyPath(other)

    def __truediv__(self, other):
        return EasyPath(other)

    def __mul__(self, other):
        return EasyPath(other)

    def __rmul__(self, other):
        return EasyPath(other)


class EasyPathTag(PosixEasyPath, WindowsEasyPath):
    def __new__(cls, *args, **kwargs):
        return object.__new__(EasyPathTag)

    def __init__(self, *tags):
        self.tags = set(tags)

    def __del__(self):
        pass

    def __rtruediv__(self, other):
        raise TypeError(f'"{self.tags_str}" can only be used in the first position')

    def __truediv__(self, other) -> EasyPath:
        other = EasyPath(other)
        return EasyPath(other, tags=set([*other.tags, *self.tags]))

    def __mul__(self, other):
        raise TypeError(f'"{self.tags_str}" can only use "/" operator')

    def __rmul__(self, other):
        raise TypeError(f'"{self.tags_str}" can only use "/" operator')


Path = EasyPathEasyPath()
Read = EasyPathTag("Read")
Write = EasyPathTag("Write")
Append = EasyPathTag("Append")
Save = EasyPathTag("Save")
Temp = EasyPathTag("Temp")
