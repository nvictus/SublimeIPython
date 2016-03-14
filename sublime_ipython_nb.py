import sublime
import sublime_plugin

from os import path
import subprocess
import tempfile
import json


class IpythonNotebookPreviewCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        view = self.view
        region = sublime.Region(0, view.size())
        contents = view.substr(region)
        tmp_dir = tempfile.gettempdir()

        # write current buffer to tmp file
        ipynb_path = path.join(tmp_dir, '%s.ipynb' % view.id())
        with open(ipynb_path, 'w') as f:
            f.write(contents )

        ipython_exec = path.expanduser('~/.virtualenvs/phd/bin/ipython')
        html_basename = path.join(tmp_dir, str(view.id()))
        cmd = [ipython_exec, 'nbconvert', '--to', 'html', '--output', html_basename, ipynb_path]
        process = subprocess.Popen(cmd)
        out, err = process.communicate()
        if out is not None:
            print out
        if err is not None:
            print err

        html_path = '%s.html' % html_basename
        print 'Notebook exported to html at %s' % html_path

        cmd = ['open', html_path]
        p = subprocess.Popen(cmd)


class IpythonNotebookRender(sublime_plugin.TextCommand):
    def run(self, edit):
        view = self.view
        region = sublime.Region(0, view.size())
        contents = view.substr(region)
        data = json.loads(contents)
        sources = [''.join(cell['source']) for cell in data['cells']]
        #view.erase(edit, region)
        window = view.window()
        for new_view in window.views():
            if new_view.name() == 'Notebook Converted':
                window.focus_view(new_view)
                new_view.erase(edit, sublime.Region(0, new_view.size()))
                break
        else:
            new_view = view.window().new_file()
            new_view.set_name('Notebook Converted')
            new_view.set_scratch(True)

        for text in sources[::-1]:
            new_view.insert(edit, 0, '\n' + text + '\n')
        new_view.set_syntax_file('Packages/SublimeIPython/IPython.tmLanguage')
        #new_view.set_read_only(True)






