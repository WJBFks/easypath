import os
import pathlib
from typing import NoReturn
from typing_extensions import NamedTuple
from .core import EasyPath, PosixEasyPath, WindowsEasyPath


class EasyPathCommandToStr(PosixEasyPath, WindowsEasyPath):
    def __del__(self):
        pass

    def __rtruediv__(self, other):
        raise TypeError(f'"ToStr" can only use "*" operator')

    def __truediv__(self, other):
        raise TypeError(f'"ToStr" can only use "*" operator')

    def __mul__(self, other):
        raise TypeError(f'"ToStr" can only be used in the last position')

    def __rmul__(self, other):
        return str(other)


class EasyPathCommandToPathlib(PosixEasyPath, WindowsEasyPath):
    def __del__(self):
        pass

    def __rtruediv__(self, other):
        raise TypeError(f'"ToPath" can only use "*" operator')

    def __truediv__(self, other):
        raise TypeError(f'"ToPath" can only use "*" operator')

    def __mul__(self, other):
        raise TypeError(f'"ToPath" can only be used in the last position')

    def __rmul__(self, other):
        return pathlib.Path(other)


class EasyPathCommandToEasyPath(PosixEasyPath, WindowsEasyPath):
    def __del__(self):
        pass

    def __rtruediv__(self, other):
        raise TypeError(f'"ToPath" can only use "*" operator')

    def __truediv__(self, other):
        raise TypeError(f'"ToPath" can only use "*" operator')

    def __mul__(self, other):
        raise TypeError(f'"ToPath" can only be used in the last position')

    def __rmul__(self, other):
        return EasyPath(other)


class EasyPathCommandReadlines(PosixEasyPath, WindowsEasyPath):
    def __del__(self):
        pass

    def __rtruediv__(self, other):
        raise TypeError(f'"Readlines" can only use "*" operator')

    def __truediv__(self, other):
        raise TypeError(f'"Readlines" can only use "*" operator')

    def __mul__(self, other):
        raise TypeError(f'"Readlines" can only be used in the last position')

    def __rmul__(self, other):
        with open(str(other), 'r') as f:
            return f.readlines()


class EasyPathCommandMakedirs(PosixEasyPath, WindowsEasyPath):
    def __del__(self):
        pass

    def __rtruediv__(self, other):
        raise TypeError(f'"Makedirs" can only use "*" operator')

    def __truediv__(self, other):
        raise TypeError(f'"Makedirs" can only use "*" operator')

    def __mul__(self, other):
        raise TypeError(f'"Makedirs" can only be used in the last position')

    def __rmul__(self, other):
        ep = EasyPath(other)
        os.makedirs(ep, exist_ok=True)
        return ep


ToStr = EasyPathCommandToStr()
ToPathlib = EasyPathCommandToPathlib()
ToPath = EasyPathCommandToEasyPath()
Readlines = EasyPathCommandReadlines()
Makedirs = EasyPathCommandMakedirs()
