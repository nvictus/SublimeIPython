import sublime, sublime_plugin
import subprocess

def extract_cell(view, line_start):
    TAG = r'^(##)(?=\s+|\Z).*'
    tags = view.find_all(TAG, 0)
    t1 = 0
    t2 = view.size()
    if tags:
        pos = [0] + [tag.a for tag in tags] + [view.size()]
        for t1, t2 in zip(pos[:-1], pos[1:]):
            if t1 <= line_start < t2: break
    return sublime.Region(t1, t2)


class EvalCellCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        view = self.view
        cursors = view.sel()
        starts = [view.line(cursor).a for cursor in cursors]
        for start in starts:
            cell_region = extract_cell(view, start)
            code = view.substr(cell_region)

            # Shell out to system python to call ipython
            p = subprocess.Popen(
                    ['/usr/bin/env', 'python', 'run_cell.py', code], 
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE, 
                    stderr=subprocess.PIPE)

            # Response
            for line in p.stdout:
                print line.rstrip()
                p.stdout.flush()


class FoldCellCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        view = self.view
        cursor = view.sel()[0]
        start = view.line(cursor).a
        cell_region = extract_cell(view, start)
        view.fold(sublime.Region(cell_region.a, cell_region.b-1))


