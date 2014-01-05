import sublime, sublime_plugin
import threading, subprocess, os, sys, signal
import re
from os.path import dirname, realpath
from functools import partial

runner = os.path.join(dirname(realpath(__file__)), 'lib', 'run_cell.py')
regex = re.compile('\x1b\[[0-9;]*m', re.UNICODE)

def extract_cell(view, cursor):
    tags = view.find_by_selector("punctuation.definition.cell.begin")
    starts = [0] + [tag.begin() for tag in tags] + [view.size()]
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

class AsyncEvalCellCommand(sublime_plugin.TextCommand):
    def __init__(self, view):
        super(AsyncEvalCellCommand, self).__init__(view)
        self.proc = None

    def on_finished(self, new_pos):
        selections = self.view.sel()
        selections.clear()
        selections.add(sublime.Region(new_pos, new_pos))
        self.view.show(self.view.sel())

    def send_to_ipython(self, cmd, cells, new_pos):
        for code in cells:           
            print "[Thread] Sending cell %s" % code.split('\n', 1)[0]

            # Shell out to the system Python to connect to IPython kernel
            self.proc = subprocess.Popen(
                cmd + [code],
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE)
            stdout, stderr = self.proc.communicate()

            if stdout:
                print "[Thread] Response:"
                print regex.sub('',stdout).strip()
            if stderr:
                print "[Thread] Error sending message to kernel: %s" \
                    % stderr.strip()
                print "[Thread] Exitcode:", self.proc.returncode
        sublime.set_timeout(partial(self.on_finished, new_pos), 0)

    def run(self, edit, env={}, stop=False):
        if self.proc and self.proc.poll() is None:
            if stop:
                print "[EvalCell] Aborting..."
                self.proc.terminate()
                #self.proc.send_signal(signal.SIGINT)
                #print "[Command] exitcode: " + str(self.proc.returncode)
            else:
                print "[EvalCell] Another cell is currently running. Request dropped."
            return

        if stop:
            return

        view = self.view
        venv_path = view.settings().get('virtual_env_path')
        if venv_path:
            cmd = [os.path.join(venv_path, 'bin', 'python'), runner]  
        else:
            cmd = ['/usr/bin/env', 'python', runner]

        selections = view.sel()
        cells = []
        for selection in selections:
            pos = selection.begin()
            cell, next_pos = extract_cell(view, pos)
            cells.append(view.substr(cell).strip('\n'))

        print "[EvalCell] Starting thread."
        self.thread = threading.Thread(
            target=self.send_to_ipython, args=(cmd, cells, next_pos))
        self.thread.start()
