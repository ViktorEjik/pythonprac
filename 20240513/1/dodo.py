
from glob import iglob, glob
from doit.tools import create_folder

HTMLINDEX = "doc/build/html/index.html"


def task_html():
    """Generate HTML docs."""
    return {
        'actions': ['sphinx-build -M html "doc/source" "doc/source/build"'],
        'file_dep': ["doc/source/index.rst", "doc/source/API.rst",
                     "mood/server/__init__.py", "mood/po/ru_RU.UTF-8/LC_MESSAGES/server.mo"],
        'targets': [HTMLINDEX]
    }


def task_erase():
    """Erase all trash"""
    return {
        'actions': ['git clean -xdf']
    }


def task_pot():
    """Re-create .pot ."""
    return {
            'actions': ['pybabel extract -o server.pot ./mood/server'],
            'file_dep': [*iglob('*.py')],
            'targets': ['server.pot'],
           }


def task_po():
    """Update translations."""
    return {
            'actions': [' pybabel update -D server -d ./mood/po -l ru_RU.UTF-8 -i server.pot'],
            'file_dep': ['server.pot'],
            'targets': ['./mood/po/ru_RU.UTF-8/LC_MESSAGES/server.po'],
           }


def task_il8n():
    """Compile translations."""
    return {
            'actions': [
                (create_folder, ['mood/po/ru_RU.UTF-8/LC_MESSAGES']),
                'pybabel compile -D server -d ./mood/po -l ru_RU.UTF-8'
                       ],
            'file_dep': ['./mood/po/ru_RU.UTF-8/LC_MESSAGES/server.po'],
            'targets': ['./mood/po/ru_RU.UTF-8/LC_MESSAGES/server.mo'],
           }

# def task_test():
#     """Update translations."""
#     return {
#             'actions': ['python -m unittest test/test.py'],
#             'file_dep': ['./mood/po/ru_RU.UTF-8/LC_MESSAGES/server.mo'],
#            }
