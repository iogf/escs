Escs
====

A modal Editor/IDE written in Python/Tk.

Escs is an IDE in the style of Emacs/Vim in the sense it doesn't demand you to use
a mouse. It was built with some goals, it should be easily extensible; users should extend Escs
in a mainstream programming language i.e Python; it should make one feel like having twenty three 
fingers on its two hands.

It implements the concept of mode states to execute specific operations based on keystrokes 
(e.g. typing text, text selection, text copy/paste). It has a first and single mode state (i.e Main)
and a second mode state (e.g Normal, Insert, Python, Golang ...). The keystrokes/functions that are common to be
performed in the latter modes are implemented in the heading state Main.

Escs allows the user to extend it with as many modes as it needs easily. Its built-in keystroke scheme should be
optmized enough for common scenaries. In case of edge cases, Escs API makes it easy to implement new workflows. 
It has a robust and simple method to remap keystrokes.

It is built on top of Python Tkinter that is a simple but powerful toolkit. Tkinter has a wide range of documentation
and several examples online. It should be a nap for one to learn enough to build nifty plugins to fullfill its daily
demands.

Features/Plugins
================

- **Python PDB Debugger**

- **Golang Delve Debugger**
    * https://github.com/go-delve/delve

- **GDB Debugger**

- **Nodejs inspect Debugger**

- **Rope Refactoring Tools**
    * https://github.com/python-rope/rope

- **Fuzzy Search**

- **Incremental Search**

- **Python Pyflakes Integration**
    * https://github.com/PyCQA/pyflakes

- **Tabs/Panes**

- **Self documenting**

- **HTML Tidy Integration**
    * http://tidy.sourceforge.net/

- **Syntax highlighting for 300+ languages**

- **Handy Shortcuts**

- **Ycmd Auto Completion**
    * https://github.com/ycm-core/ycmd

- **Quick Snippet Search**

- **Smart Search with The Silver Searcher**
    * https://github.com/ggreer/the_silver_searcher

- **File Manager**

- **Python Static Type Checker**
    * http://mypy-lang.org/

- **Terminal-like**

- **Irc Client Plugin**

- **Find Function/Class Definition**

- **Python Vulture Integration**
    * https://github.com/jendrikseipp/vulture

- **Python Auto Completion**
    * https://github.com/davidhalter/jedi

Install
=======

~~~
pip install escs
~~~


