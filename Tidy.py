from sublime_plugin import TextCommand
from sublime import Region
from subprocess import call
from os.path import abspath, expanduser, exists, join
from sys import path
try:
    # ST2/Python 2.6
    from StringIO import StringIO
except ImportError:
    # ST3/Python 3.3
    from io import StringIO

# load the git submodule
extra = abspath('PythonTidy')
if not exists(join(extra, '.git')):
    call(['git', 'submodule', 'init'])
    call(['git', 'submodule', 'update'])

# tweak path to allow importing PythonTidy from the git submodule
path.insert(0, extra)
import PythonTidy
import PythonTidyWrapper
path.remove(extra)


def setup():
    xml = expanduser('~/.pythontidy.xml')
    if exists(xml):
        config = PythonTidyWrapper.Config(file=xml)
        config.to_pythontidy_namespace()


class PythonTidyCommand(TextCommand):

    def run(self, edit):
        setup()
        view = self.view
        region = Region(0, view.size())
        encoding = view.encoding()
        if not encoding or encoding == u'Undefined':
            encoding = view.settings().get('default_encoding')
        source = StringIO(view.substr(region).encode(encoding))
        output = StringIO()
        PythonTidy.tidy_up(source, output)
        view.replace(edit, region, output.getvalue().decode(encoding))

