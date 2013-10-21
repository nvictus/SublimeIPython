# codecells

Sublime Text 2 plugin to evaluate cells of code in a running IPython kernel. 

This will let you work both in the editor and play with your favorite REPL interactively.

## Setup
Clone this repo into Sublime's Packages directory.

Go to *Preferences* -> *Key Bindings - User* and add the following entry:

```json
{ "keys": ["super+enter"], "command": "eval_cell", "context": [{
      "key": "selector",
      "operator": "equal",
      "operand": "source.python"}]
}
```

## Usage
Make sure you are running an instance of one of ipython console, qtconsole or notebook.

Now, when you set your document's syntax to **CodeCells**, you can press **cmd-enter** to evaluate code between two `##` tags! The cursor will jump to the next cell.

##Example

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

While the `##` tags make it easy to embed cells into vanilla python scripts, it would be nice to:

- extend this to run ipython cells and cell magics `%%` and add ipython-specific syntax highlighting

- have a convert-to-notebook feature

- broadcast errors to the stdout of the running front-end (right now they are printed in sublime's console)

- support interactive input from the running front-end

- windows support