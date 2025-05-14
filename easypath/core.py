from io import TextIOWrapper
from typing import Any, Literal, Self, TypeAlias, overload
from common import OpenTextMode


class EasyPathToStr:
    ...


class EasyPath:
    def __init__(self, path=None, special=None):
        self.path = path
        self.file: TextIOWrapper = None
        self.special = special

    @overload
    def __truediv__(self, path: str) -> Self:
        ...

    @overload
    def __truediv__(self, wjPath: Self) -> Self:
        ...

    @overload
    def __truediv__(self, wjPath: "EasyPathToStr") -> str:
        ...

    @overload
    def __truediv__(self, wjPath: Any) -> Self:
        ...

    def __truediv__(self, other: str | Self | "EasyPathToStr" | Any):
        if type(other) == str:
            if self.path == None:
                return EasyPath(other, special=self.special)
            return EasyPath(self.path + "/" + other, special=self.special)
        elif isinstance(other, EasyPath):
            if self.path == None:
                return EasyPath(other.path, special=self.special)
            return EasyPath(self.path + "/" + other.path, special=self.special)
        elif isinstance(other, EasyPathToStr):
            return str(self)
        else:
            if self.path == None:
                return EasyPath(str(other), special=self.special)
            return EasyPath(self.path + "/" + str(other), special=self.special)

    def __str__(self) -> str:
        if self.path == None:
            return ""
        return self.path

    def open(self, mode: OpenTextMode = "r") -> TextIOWrapper:
        self.file = open(self.path, mode)
        return self.file

    def __enter__(self) -> TextIOWrapper:
        if self.special == "Read":
            self.file = open(self.path, "r")
        elif self.special == "Write":
            self.file = open(self.path, "w")
        elif self.special == "Append":
            self.file = open(self.path, "a")
        return self.file

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file.close()
