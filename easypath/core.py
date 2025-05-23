import atexit
from io import TextIOWrapper
from logging import warning
import os
import pathlib
import signal
from typing_extensions import List, Any, Literal, Self, TypeAlias, overload
from .common import OpenTextMode
import sys


class EasyPathToStr:
    ...


p = pathlib.Path()


class EasyPath(pathlib.Path):

    def __new__(cls, *args, **kwargs):
        # 如果python>=3.12
        if sys.version_info >= (3, 12):
            if cls is EasyPath:
                cls = WindowsEasyPath if os.name == 'nt' else PosixEasyPath
            return object.__new__(cls)
        else:
            if cls is EasyPath:
                cls = WindowsEasyPath if os.name == 'nt' else PosixEasyPath
            self = cls._from_parts(args, init=False)
            if not self._flavour.is_supported:
                raise NotImplementedError("cannot instantiate %r on your system" % (cls.__name__,))
            self._init()
            return self

    def __init__(self, *paths: List[str], tags: set = None, cleanup=None):
        # print(paths)
        self.tags = tags if tags is not None else set()
        self.cleanup = cleanup
        if sys.version_info >= (3, 12):
            super().__init__(*paths)
        for path in paths:
            if isinstance(path, PosixEasyPath) or isinstance(path, WindowsEasyPath):
                self.tags = set([*self.tags, *path.tags])
                if path.cleanup != None:
                    atexit.unregister(path.cleanup)

        if "Temp" in self.tags:
            def cleanup():
                try:
                    path = str(self)
                    os.remove(path)
                except Exception as e:
                    warning(f"Failed to remove temp file: {e}")
            self.cleanup = cleanup
            atexit.register(self.cleanup)

    @property
    def tags_str(self) -> str:
        return ", ".join(self.tags)

    def __str__(self):
        path = super().__str__()
        if "Save" in self.tags or "Temp" in self.tags:
            dirs = os.path.dirname(path)
            os.makedirs(dirs, exist_ok=True)
        return path

    def __rtruediv__(self, other) -> "EasyPath":
        other = EasyPath(other)
        return EasyPath(self, other)

    def __truediv__(self, other) -> "EasyPath":
        other = EasyPath(other)
        return EasyPath(self, other)

    def __enter__(self) -> TextIOWrapper:
        if "Read" in self.tags:
            self.file = open(self, "r")
        elif "Write" in self.tags:
            self.file = open(self, "w")
        elif "Append" in self.tags:
            self.file = open(self, "a")
        elif self.tags is None:
            self.file = open(self, "r")
        else:
            raise ValueError("Invalid command")
        return self.file

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file.close()


class PosixEasyPath(EasyPath, pathlib.PurePosixPath):
    __slots__ = ()


class WindowsEasyPath(EasyPath, pathlib.PureWindowsPath):
    __slots__ = ()

    def is_mount(self):
        raise NotImplementedError("Path.is_mount() is unsupported on this system")
