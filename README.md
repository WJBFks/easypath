# EasyPath

[English Version](./README.en.md)

一个更容易使用的Python路径库。取代`os.path`和`pathlib.Path`。

## 使用

该库的核心是`EasyPath`类，继承自`pathlib.Path`，并添加了一些方便的方法。你有以下几种方式可以创建一个`EasyPath`对象：

```python
import pathlib
from easypath import EasyPath, Path

# 1. 使用字符串
ep = EasyPath('/path/to/file')

# 2. 使用另一个EasyPath对象
ep = EasyPath(ep)

# 3. 使用pathlib.Path对象
path = pathlib.Path('/path/to/file')
ep = EasyPath(path)

# 4. 使用'/'运算符（推荐）
ep = Path / '/path/to/file'
```

其中，推荐使用第4种方式，因为其省去了**烦人的左右括号**，并且你可以通过`/`使用`Path`来链接所有`PathLike`的对象，如`str`、`Path`、`EasyPath`等。

## 方法

### 1. 路径拼接

你可以使用`/`运算符来拼接路径，如：

```python
from easypath import Path
import pathlib
home = EasyPath('/home/user')
code_path = pathlib.Path('workspace/code')
ep = root / code_path / 'easypath/core/main.py'
# 一个更常用的写法是：
ep = Path / 'workspace/code' / 'easypath/core/main.py'
```

这个功能是`pathlib.Path`本来就有的，`EasyPath`对其做了部分增强

### 2. 标签

你可以为一个`EasyPath`对象添加标签，这些标签会在特定的时候发挥对应的作用，这些标签的方式是使用`/`进行连接，一个`EasyPath`对象可以有多个标签，通常建议把标签放在最开头，如：
```python
from easypath import Read, Write
log_path = 'logs/test.log'
write_path = Write / log_path # 表示一个写日志的路径
# 被标记为'Write'的路径，可以直接用with语句进行写操作
with write_path as f:
    f.write('hello world')
# 被标记为'Read'的路径，可以直接用with语句进行读操作
with Read / log_path as f:
    print(f.read())
```
实际上，所有的标签都可以接受`str`、`Path`、`EasyPath`等对象，并且可以嵌套使用，其会自动转换为`EasyPath`对象

#### 3. 指令

与`标签`不同，`标签`只是用于标记路径，其不会对路径进行任何操作，需要与其他方法配合使用，而`指令`则是对路径**立即**进行操作，指令使用`*`进行连接，通常建议把指令放在最末尾，因为很多指令会改变对象的类型，如：

```python
from easypath import Path, ToStr, Readlines
ep = Path / 'logs/test.log'
ep_str = ep * ToStr   # 将`EasyPath`对象转换为`str`对象
lines = ep * Readlines # 读取文件内容，并返回一个列表list[str]
```

大部分的`指令`都可以接受`str`、`Path`、`EasyPath`等对象，其会尝试将其自动转换为支持的对象并立即执行指令。

## 标签列表

| 标签 | 说明 |
| ---- | ---- |
| `Read` | 读取文件 |
| `Write` | 写入文件 |
| `Append` | 追加写入文件 |
| `Save` | 自动创建目录 |
| `Temp` | 创建临时文件 |

### Save标签

`Save`标签会尝试创建目录，如果目录已经存在，则不会报错，如果目录创建失败，则会抛出异常，如：

```python
import torch
from easypath import Path, Save
save_path = Save / 'train' / 'checkpoint'
tensor = torch.tensor([1, 2, 3])
torch.save(tensor, save_path) # 将tensor保存到save_path指定的目录下
```
该标签不会立即尝试创建目录，而是当**每次**尝试访问该路径时，才会尝试创建目录。这样做的好处是，如果在运行过程中，目录被删除了，那么可以自动重新创建目录，而不需要手动重新创建。如果你希望立即创建目录且仅尝试创建一次，可以使用`Mkdir`指令：
```python
from easypath import Path, Mkdir
save_path = 'train' / 'checkpoint' * Mkdir
```

### Temp标签

`Temp`标签会创建一个临时文件，该临时文件会在程序结束时自动删除，如：

```python
from easypath import Temp, Write
temp_path = Temp / 'temp.txt'
with Write / temp_path as f:
    f.write('hello world')
# 程序退出，`temp.txt`文件会被自动删除
```

注意：该操作只会在程序结束时自动删除，如果在程序运行过程中，临时文件被手动删除，那么该操作将不再生效。此外，该操作只会删除临时文件，不会删除临时目录。

## 指令列表

| 指令 | 说明 |
| ---- | ---- |
| `ToStr` | 转为`str` |
| `ToPathlib` | 转为`ToPathlib` |
| `ToPath` | 转为`ToPath` |
| `Readlines` | 读取文件，返回list[str] |
| `Makedirs` | 立即创建目录 |

## 更新日志

- v0.1.0: 初始版本，实现了标签和指令的基本功能，并将中文作为默认文档，已在python3.9和3.12通过测试