from importlib import import_module

from setuptools import setup, find_packages

setup(
    name = 'enumjson',
    version = import_module('enumjson').__version__,
    author = 'Satoshi Nihonyanagi',
    author_email = 'sakurahilljp@gmail.com',
    url = 'https://github.com/sakurahilljp/enumjson',
    license = 'BSD',
    description = 'Enumerate JSON element in large JSON files',
    long_description = open('README.md').read(),

    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],

    packages = find_packages(),
)
