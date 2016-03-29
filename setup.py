# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import sys
import os


NAME = 'myrpg'
KEYWORDS = 'rpg engine editor'
DESC = '2D RPG game engine and editor'
URL = 'https://github.com/linkdd/myrpg'
AUTHOR = 'David Delassus'
AUTHOR_EMAIL = 'david.jose.delassus@gmail.com'
LICENSE = 'MIT'
ENTRY_POINTS = [
    'myrpg-game-launch = myrpg.game:main',
    'myrpg-editor = myrpg.editor.main:main'
]
REQUIREMENTS = [
    'b3j0f.conf',
    'six',
    'pyglet',
    'PySide'
]


def get_cwd():
    filename = sys.argv[0]
    return os.path.dirname(os.path.abspath(os.path.expanduser(filename)))


def get_version(default='0.1'):
    sys.path.append(get_cwd())
    import myrpg

    return getattr(myrpg, '__version__', default)


def get_long_description():
    path = os.path.join(get_cwd(), 'README.rst')
    desc = None

    if os.path.exists(path):
        with open(path) as f:
            desc = f.read()

    return desc


def get_test_suite():
    path = os.path.join(get_cwd(), 'tests')

    return 'tests' if os.path.exists(path) else None


setup(
    name=NAME,
    keywords=KEYWORDS,
    version=get_version(),
    url=URL,
    description=DESC,
    long_description=get_long_description(),
    license=LICENSE,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    packages=find_packages(),
    package_dir={'': get_cwd()},
    entry_points={
        'console_scripts': ENTRY_POINTS
    },
    test_suite=get_test_suite(),
    install_requires=REQUIREMENTS
)
