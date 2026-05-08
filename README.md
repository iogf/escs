Escs
====

A modal Text Editor/IDE written in Python/Tk.

Escs is in the style of Vim/Emacs in regard it being modal or not demanding to use a mouse. 
It has some similarities with Vim like Normal, Insert modes and keystrokes to move cursor around.

It was built with some goals, it should be easily extensible; users should extend and configure 
Escs in a mainstream programming language (e.g Python). . 

Escs doesn't demand you to have twenty three fingers it makes you feel like having twienty four 
fingers in your hands.

Escs has an optmized scheme of keystrokes/operations it has a single major mode (i.e Main) also 
minor modes (e.g Normal, Insert, Extra). Operations that are often used and common  when working 
with a text editor are implemented in Main mode.

The Syntax Highlighter plugin makes it easy to create themes. It integrates with Python/Pygments 
to perform syntax hgihlighting for documents.

There are several built-in modes for programming languages like Python, Golang, Javascript.'
It is straight to implement custom modes or extend built-in modes to work with specific file types.

Escs integrates with Ycmd to do code completion it is simple to use other type of engines to perform 
several tasks. It has also a built-in plugin to perform code completion through Jedi.

There is a built-in file manager it is handy to inspect directories, files. There are keystrokes for 
performing common file operations (e.g move, rename, delete). It is simple to organize project files.

Escs has built-in integration with an asynchronous framework to implement tools that demand working 
with pipes or sockets. Users can spawn processes then send and receive data in an asynchronous manner.

The plugin architecture is nifty it is straight to extend Escs with custom functionalities or tools. 
It even has a built-in IRC client plugin.

There is a built-in terminal-like plugin that allows to execute commands through a Bash process. 

![screenshot-1](screenshot-1.png)

Features/Plugins
================

- **Python PDB Debugger**

- **Golang Delve Debugger**
    * https://github.com/go-delve/delve

- **GDB Debugger**

- **Nodejs inspect Debugger**

- **Rope Refactoring Tools**
    * https://github.com/python-rope/rope

- **Incremental Search**

- **Python Pyflakes Integration**
    * https://github.com/PyCQA/pyflakes

- **Tabs/Panes**

- **Self documenting**

- **Syntax Highlighter for 300+ languages**

- **Handy Shortcuts**

- **Ycmd Auto Completion**
    * https://github.com/ycm-core/ycmd

- **Quick Snippet Search**

- **The Silver Searcher**
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


