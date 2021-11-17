# Project structure

First thing to strike me the structure of the code. It's atypical of most
python packages in that I'm used to looking at (in my work or form the wider
community).

The covnention in python is actually more of a rule because a lot of tooling
around python will rely on baked in assumptions that your project will follow
python conventions. E.g. You'll have the project root directory and it'll have
a folder in it which is the python package's name (or slightly less commonly) a
directory call `src` where all of the source code (not the tests) lives. And
you'll be editing code in there, and you'll be able to run the code from there
as well.

I bring this up because I should be able (IMO) to `cd` into the project
directory and run any set of the units tests I want without having to do any
further setup - which I wasn't able to do with this code.

See:

```
$ pytest
========================================= test session starts ==========================================
platform linux -- Python 3.10.0, pytest-6.2.5, py-1.11.0, pluggy-1.0.0
rootdir: /home/mlittlej/github/flamekebab/TCW-Output-Formats
collected 0 items / 1 error                                                                            

================================================ ERRORS ================================================
____________________________ ERROR collecting tests/test_transcode_tools.py ____________________________
ImportError while importing test module '/home/mlittlej/github/flamekebab/TCW-Output-Formats/tests/test_transcode_tools.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
../../../.pyenv/versions/3.10.0/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_transcode_tools.py:1: in <module>
    import tcw_transcode_tools
E   ModuleNotFoundError: No module named 'tcw_transcode_tools'
======================================= short test summary info ========================================
ERROR tests/test_transcode_tools.py
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
=========================================== 1 error in 0.04s ===========================================
```

Basically python doesn't know where to find the module you've written using
normal python package lookup rules. I don't know how you're setup in your
machine but it don't work on mine out of the box.

This article does a reasonable job of explaining the python project layout
conventions and a little bit about why they're set-up that way:

https://dev.to/codemouse92/dead-simple-python-project-structure-and-imports-38c6

Also, pay attention to what `__init__.py` (and later `__main__.py`) files are,
because they're important, especially around being able to import files from
one place to another. They're in the article, but the python documentation
does a good job of explaining them too.

Anyway, to be able to run your unit-tests using pytest for me I had to
restructure your files and the aforementioned `__init__.py` files. You can see
the changes in commit `6c7a5d3`. After that I got them working and all thwey
all passed, which is a good start.
