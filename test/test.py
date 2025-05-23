from time import sleep
from easypath import EasyPath
from easypath import Read, ToPath, Path, Write, Append, Readlines, Makedirs, Temp
import pathlib
import os

if __name__ == '__main__':
    temp = Temp / 'test'
    t = Write / temp / 'test.txt'
    with t as f:
        f.write('hello world')
