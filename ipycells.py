from __future__ import print_function
import sublime_plugin, sublime

import subprocess
import os.path
import glob
import sys
import re
from os.path import dirname, abspath
from functools import partial

SETTINGS_FILE = "IPython.sublime-settings"
runner = os.path.join(dirname(abspath(__file__)), 'bin', 'run_cell.py')


def extract_cell(view, cursor):
    tags = view.find_by_selector("punctuation.section.cell.begin")
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
        
        pyexe_path = view.settings().get('python_executable', None)
        if pyexe_path:
            cmd = [os.path.join(pyexe_path), runner]  
        else:
            if os.name == 'nt':
                cmd = ['python.exe', runner]
            else:
                cmd = ['/usr/bin/env', 'python', runner]

        for selection in selections:
            pos = selection.begin()
            cell, next_pos = extract_cell(view, pos)
            code = view.substr(cell).strip('\n')
            head, code = code.split('\n', 1)    

            print("sending %s" % head)
            # Call the system Python to connect to IPython kernel
            p = subprocess.Popen(
                    cmd + [code],
                    stdout=subprocess.PIPE, 
                    stderr=subprocess.PIPE)
            
            # Response
            if p.stdout:
                for line in p.stdout:
                    print(line.decode('utf-8').rstrip())
                    p.stdout.flush()
                print()

            if p.stderr:
                # strip the ansi color codes from the ultraTB traceback
                regex = re.compile('\x1b\[[0-9;]*m', re.UNICODE)
                for line in p.stderr: 
                    print(regex.sub('', line.decode('utf-8').rstrip()))
                    p.stderr.flush()
                print()

        selections.clear()
        selections.add(sublime.Region(next_pos,next_pos))


class ToggleFoldCellCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        view = self.view
        selections = view.sel()
        for selection in selections:
            region = selection
            if region.empty():
                region = sublime.Region(selection.a-1, selection.a+1)

            unfolded = view.unfold(region)
            if len(unfolded) == 0:  # already unfolded
                pos = selection.begin()
                cell, next_pos = extract_cell(view, pos)
                lines = view.lines(cell)
                region_to_fold = sublime.Region(lines[1].a-1, lines[-1].b)
                view.fold(region_to_fold)


class SetJupyterPythonExecutable(sublime_plugin.TextCommand):
    def set_pyexe(self, path):
        settings = self.view.settings()
        settings.set('python_executable', os.path.abspath(os.path.expanduser(path)))
         
    def run(self, edit):
        settings = self.view.settings()
        text = settings.get('python_executable')
        self.view.window().show_input_panel(
            'Path to Jupyter Python executable', text, self.set_pyexe, None, None)





# def scan_for_virtualenvs(venv_paths):
#     bin_dir = "Scripts" if os.name == "nt" else "bin"
#     found_dirs = set()
#     for venv_path in venv_paths:
#         p = os.path.expanduser(venv_path)
#     if os.path.exists(venv_path):
#         pattern = os.path.join(p, "*", bin_dir, "activate_this.py")
#         found_dirs.update(list(map(os.path.dirname, glob.glob(pattern))))
#     return sorted(found_dirs)

# class SetVirtualenvCommand(sublime_plugin.TextCommand):
#     def _scan(self):
#         settings = sublime.load_settings(SETTINGS_FILE)
#         venv_paths = settings.get("python_virtualenv_paths", [])
#         return scan_for_virtualenvs(venv_paths)

#     def set_virtualenv(self, choices, index):
#         if index == -1:
#             print("no virtualenvs found")
#             return
#         (name, directory) = choices[index]
#         activate_file = os.path.join(directory, "activate_this.py")
#         python_executable = os.path.join(directory, "python")
#         path_separator = ":"
#         if os.name == "nt":
#             python_executable += ".exe"  # ;-)
#             path_separator = ";"

#         #cmd = [python_executable, runner]
#         self.view.settings().set('virtualenv_path', directory)

#     def run(self, edit):
#         choices = self._scan()
#         nice_choices = [[path.split(os.path.sep)[-2], path] for path in choices]
#         self.view.window().show_quick_panel(
#             nice_choices, 
#             partial(self.set_virtualenv, nice_choices)
#         )


# class SetVirtualenvCommand(sublime_plugin.TextCommand):
#     def set_venv_path(self, venv):
#         settings = self.view.settings()
#         settings.set('virtual_env_path', os.path.expanduser(venv))   
         
#     def run(self, edit):
#         settings = self.view.settings()
#         text = settings.get('virtual_env_path') or os.path.expanduser('~/.virtualenvs/')
#         self.view.window().show_input_panel(
#             'Path to virtualenv', text, self.set_venv_path, None, None)

# self.window.run_command("repl_open",
#     {
#         "encoding":"utf8",
#         "type": "subprocess",
#         "autocomplete_server": True,
#         "extend_env": {
#             "PATH": directory + path_separator + "{PATH}",
#             "SUBLIMEREPL_ACTIVATE_THIS": activate_file,
#             "PYTHONIOENCODING": "utf-8"
#         },
#         "cmd": [python_executable, "-u", "${packages}/SublimeREPL/config/Python/ipy_repl.py"],
#         "cwd": "$file_path",
#         "encoding": "utf8",
#         "syntax": "Packages/Python/Python.tmLanguage",
#         "external_id": "python"
#      })

