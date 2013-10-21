# codecells

Sublime Text 2 plugin to evaluate cells of Python code in a running IPython [kernel](http://nbviewer.ipython.org/urls/raw.github.com/ipython/ipython/1.x/examples/notebooks/Frontend-Kernel%20Model.ipynb). 

This will let you both work in the editor and play with your favorite REPL environment interactively! :)

## Setup
Clone this repo into Sublime's Packages directory.

## Usage
Make sure you are running an instance of one of ipython console, qtconsole or notebook. The plugin will connect to the most recently launched kernel on your system.

Now, when you set your document's syntax to **CodeCell**, you can press **cmd/ctrl-enter** to evaluate code between two `##` tags! The cursor will jump to the next cell. Place muliple cursors in multiple cells to run them all in succession.

### Examples of "cells"

```python

## cell 1
x = 5
doFoo(x)

## cell 2
x = 10
y = 9000
doBar(x,y)
```

##Todo

The `##` tags make it easy to embed cells into vanilla Python scripts. However, it would be nice to:

- extend this to run ipython cells and cell magics `%%` and add ipython-specific syntax highlighting

- broadcast errors to the stdout of the running front-end (right now they are printed in sublime's console and the ultraTB tracebacks are all mangly)

- support interactive input from the running front-end

- add a convert-to-notebook feature

- code folding of cells 

- windows support

- fix bugs!
