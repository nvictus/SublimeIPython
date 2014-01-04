import sublime, sublime_plugin
import os, subprocess
from os.path import dirname, abspath
import re

runner = os.path.join(dirname(abspath(__file__)), 'lib', 'run_cell.py')

def extract_cell(view, cursor):
    tags = view.find_by_selector("punctuation.definition.cell.begin")
    starts = [0] + [tag.a for tag in tags] + [view.size()]
    region = None
    for begin, end in zip(starts[:-1], starts[1:]):
        if begin <= cursor < end:
            region = sublime.Region(begin, end)
            next = end
            break
    if not region:
        if cursor == end:
            region = sublime.Region(begin, end)
            next = end
        else:
            raise ValueError(
                "Position (%d,%d) could not be matched to a cell." 
                % view.rowcol(cursor))
    return region, next

class EvalCellCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        view = self.view
        selections = view.sel()
        cmd = ['/usr/bin/env', 'python', runner]

        for selection in selections:
            pos = selection.begin()
            cell, next_pos = extract_cell(view, pos)
            code = view.substr(cell).strip('\n')

            print             
            print "sending %s" % code.split('\n', 1)[0]

            # Shell out to the system Python to connect to IPython kernel
            p = subprocess.Popen(
                    cmd + [code],
                    stdout=subprocess.PIPE, 
                    stderr=subprocess.PIPE)
            
            # Response
            if p.stdout:
                for line in p.stdout:
                    print line.rstrip()
                    p.stdout.flush()

            if p.stderr:
                # strip the ansi color codes from the ultraTB traceback
                regex = re.compile('\x1b\[[0-9;]*m', re.UNICODE)
                for line in p.stderr: 
                    print regex.sub('', line).rstrip()
                    p.stderr.flush()

        selections.clear()
        selections.add(sublime.Region(next_pos,next_pos))

class FoldCellCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        view = self.view
        selections = view.sel()
        for selection in selections:
            pos = selection.begin()
            cell, next_pos = extract_cell(view, pos)
            lines = view.lines(cell)
            region_to_fold = sublime.Region(lines[1].a-1, lines[-1].b)
            view.fold(region_to_fold)

class KillCellCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        p = self.view.proc
        p.terminate()

