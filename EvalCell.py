import sublime, sublime_plugin
import subprocess

# iPyCodeCells

class EvalCellCommand(sublime_plugin.TextCommand):
    def selected_cell(self):
        v = self.view
        line = v.line(v.sel()[0])

        TAG = r'^\Q##\E(?=\s*|\n)'
        tags = v.find_all(TAG, 0L)
        if tags:
            pos = [0] + [tag.a for tag in tags] + [v.size()]
            for t1, t2 in zip(pos[:-1], pos[1:]):
                if t1 <= line.a < t2:
                    break
            cell = sublime.Region(t1, t2)
        else:
            cell = sublime.Region(0, self.view.size())

        return self.view.substr(cell)      

    def run(self, edit):
        # use regex w/ ST2 API to find the cell boundaries and extract the code
        code = self.selected_cell()

        # We could try to communicate with an existing ipy process directly, but 
        # the IPython module has a complete kernel manager for that. :)

        # However, ST2's embedded interpreter does not support IPython.

        # So to use the kernel manager, let's execute... a python script!
        p = subprocess.Popen(['/usr/bin/env', 'python', './lib/run_cell.py', code], 
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE)

        # Response
        for line in p.stdout:
            print line.rstrip()
            p.stdout.flush()

