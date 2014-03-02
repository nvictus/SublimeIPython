# sublime-ipython

This Sublime Text 2/3 plugin lets you evaluate blocks of code in a running IPython [kernel](http://nbviewer.ipython.org/urls/raw.github.com/ipython/ipython/1.x/examples/notebooks/Frontend-Kernel%20Model.ipynb), connecting the editor to your REPL workflow. 

You may find it useful to run code cells from the editor when it would be inconvenient to type at the console and overkill to switch to the json-based notebook format, e.g. interactive experimentation, one-off scripts, debugging existing scripts. The simple cell delimiter `##` is just a comment, so pure Python cells are fully compatible with vanilla Python files.

Both line and cell magics are supported.

## Install
Requires IPython 1.0+

Clone this repo into Sublime's _Packages_ directory.

If you don't know where that folder is, open Sublime Text, go to _Preferences_ > _Browse Packages_ and see where you end up.

## Usage
Make sure you are running an instance of one of ipython `console`, `qtconsole` or `notebook`. The plugin will connect to the most recently launched kernel on your system.

Now, if you set your document's syntax highlighting to **IPython** or use the .ipy file extension, evaluate code between any two `##` tags by pressing **cmd+enter** on Mac or **ctrl+enter** on Linux. The cursor will jump to the next cell. Place muliple cursors in multiple cells to run them all in succession. Confirmation and error tracebacks will appear in Sublime's console (to pull that up, type **ctrl+"\`"**).

### Examples of code cells

```python

## cell 1
x = 5
doFoo(x)

## cell 2
x = 10
y = 9000
doBar(x,y)
%load_ext rmagic
X = np.array([1,2,3,4,5])
Y = np.random.rand(5)

## cell magic
%%R -i X,Y -o XYcoef
XYlm = lm(Y~X)
XYcoef = coef(XYlm)
```
Individual cells can be folded and unfolded using **cmd+"."**.

If you are running IPython inside a virtual environment, you can provide the path of your active virtualenv to SublimeIPython using **cmd+opt+v** (**ctrl+alt+v**) so that the appropriate Python binary is called.


##Todo

- Currently, ST2 blocks while a cell is evaluating. This should be asynchronous.

- Provide selection of running kernel instances or launch a new one.

- Convert-to-notebook feature

- Key binding to toggle pdb breakpoints

- Code completion


It would also be nice to:

- broadcast errors and output to the interactive front-end (right now errors are printed in sublime's console)

- forward input/raw_input requests to the interactive front-end

- add windows support



## Similar projects

- [SublimeIPythonNotebook](https://github.com/maximsch2/SublimeIPythonNotebook)
- [SublimeIPython](https://github.com/iambus/SublimeIPython)
- [vim-ipython](https://github.com/ivanov/vim-ipython)
- [SublimeREPL](https://github.com/wuub/SublimeREPL)
