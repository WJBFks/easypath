from setuptools import setup

import easypath

with open("README.md") as file:
    readme = file.read()

setup(
    name="easypath",
    version=easypath.__version__,
    description="A Python library for easier use of the path. To replace os.path and pathlib.Path.",
    author="WJBFks",
    author_email="",
    url="",
    packages=['easypath'],
    license="MIT",
    long_description=readme,
    setup_requires=['setuptools'],
    python_requires=">=3.9",
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ]
)
