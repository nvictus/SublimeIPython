# sublime-ipython

Sublime Text 2 plugin to evaluate cells of code in a running IPython [kernel](http://nbviewer.ipython.org/urls/raw.github.com/ipython/ipython/1.x/examples/notebooks/Frontend-Kernel%20Model.ipynb). 

It's about time your favorite editor got in touch with your favorite interpreter! :)

## Install
Clone this repo into Sublime's _Packages_ directory.

If you don't know where that folder is, open Sublime Text, go to _Preferences_ > _Browse Packages_ and see where you end up.

## Usage
Make sure you are running an instance of one of ipython `console`, `qtconsole` or `notebook`. The plugin will connect to the most recently launched kernel on your system.

Now, if you set your document's syntax highlighting to **IPython** (or use the .ipy file extension), you can press **cmd+enter** on Mac (**ctrl+enter** on Linux) to evaluate code between any two `##` tags. The cursor will jump to the next cell. Place muliple cursors in multiple cells to run them all in succession. Confirmation and error tracebacks will appear in Sublime's console (to pull that up, type **ctrl+"\`"**).

### Examples of "cells"

```python

## cell 1
x = 5
doFoo(x)

## cell 2
x = 10
y = 9000
doBar(x,y)
%load_ext rmagic

## cell magic
%%R -i X,Y -o XYcoef
XYlm = lm(Y~X)
XYcoef = coef(XYlm)

```
The `##` tags make it easy to embed cells into vanilla Python scripts. Individual cells can be folded and unfolded using **cmd+"."**.

If you are running IPython inside a virtual environment, you can provide the path of your active virtualenv to SublimeIPython using **cmd+opt+v** (**ctrl+alt+v**) so that the appropriate python binary and site-packages are used.

I have only briefly tested ST3, but it seems to work.

##Todo

Currently, Sublime Text blocks while a cell is evaluating. This should be asynchronous.

It would also be nice to:

- broadcast errors and output to the interactive front-end (right now errors are printed in sublime's console)

- forward input/raw_input requests to the interactive front-end

- add a convert-to-notebook feature

- add windows support

- fix bugs!
