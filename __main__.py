#!/usr/local/bin/py -3

import ctypes
import pathlib
import shutil
import subprocess
import types
import typing
import yaml

from distutils import sysconfig
from pprint import pprint

from . import PyTypeObject, PyObject


_CELLAR = subprocess.getoutput('brew --cellar')
_CACHE = pathlib.Path(__file__).with_name('Headers')


# _PREFIX = pathlib.Path(sysconfig.PREFIX).with_name('Current')
# for prefix in map(pathlib.Path,
#                   [sysconfig.PREFIX,
#                    sysconfig.EXEC_PREFIX,
#                    sysconfig.BASE_PREFIX,
#                    sysconfig.BASE_EXEC_PREFIX,
#                    ]):
#     assert prefix.exists()
#     print(prefix.resolve())


# pprint(sysconfig.get_config_vars())


def _find_python_install_info() -> typing.Iterator[types.SimpleNamespace]:
    info = yaml.safe_load_all(
        subprocess.getoutput('{0} {1}'.format(
            command := _CACHE.with_name('generate_sources.sh'),
            command.with_name('data'),
            )))

    for document in info:
        yield types.SimpleNamespace(**document)


def _parse_header(header: pathlib.Path) -> dict:
    with open(header) as fp:
        return sysconfig.parse_config_h(fp)


def _find_headers(src: pathlib.Path) -> typing.Iterator:
    for path in src.iterdir():
        if path.is_dir():
            yield from _find_headers(path)
        else:
            assert path.is_file()
            if path.suffix == '.h':
                yield path


def _copy_headers():
    if not _CACHE.exists():
        _CACHE.mkdir()

    for ns in _find_python_install_info():
        formula = pathlib.Path(_CELLAR, ns.formula)
        keg = pathlib.Path(formula, ns.keg)
        cache = pathlib.Path(_CACHE, ns.formula, ns.keg)
        headers = pathlib.Path(
            keg,
            'Frameworks', 'Python.framework',
            'Versions', 'Current', 'Headers',
            )

        if not cache.exists():
            cache.mkdir(parents = True)

        for header, exports in ns.headers.items():
            assert (src := pathlib.Path(headers, header)).exists()
            if (dest := pathlib.Path(cache, header)).parent != cache:
                if not dest.parent.exists():
                    dest.parent.mkdir(parents = True)

            print(dest)
            shutil.copy(src, dest)
            pprint(_parse_header(dest))
            print()

        # for symbol in exports:
        #     try:
        #         tp = PyTypeObject.in_dll(ctypes.pythonapi, symbol)
        #         # print(tp)
        #     except ValueError as exc:
        #         print(f'{header}: {exc}')


if __name__ == '__main__':
    _copy_headers()
