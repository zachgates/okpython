#!/usr/local/bin/py -3

import ctypes
import pathlib
import subprocess
import yaml

from . import PyTypeObject, PyObject


cellar = subprocess.getoutput('brew --cellar')
for document in yaml.safe_load_all(
    subprocess.getoutput('%s %s' % (
        command := pathlib.Path(__file__).with_name('generate_sources.sh'),
        command.with_name('data'),
        ))):

    locals().update(document)
    for include, exports in headers.items():
        assert (header := pathlib.Path(cellar, formula, keg,
                                       'Frameworks', 'Python.framework',
                                       'Headers', include,
                                       )).exists()
        for symbol in exports:
            try:
                tp = PyTypeObject.in_dll(ctypes.pythonapi, symbol)
            except ValueError as exc:
                print(f'{header}: {exc}')
            # else: print(str(tp.tp_name, 'utf-8'))
