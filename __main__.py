#!/usr/local/bin/py -3

import ctypes
import pathlib
import subprocess
import typing
import yaml

from distutils import sysconfig
from pprint import pprint

from . import PyTypeObject, PyObject


CELLAR = subprocess.getoutput('brew --cellar')
PY_INCLUDE = pathlib.Path(sysconfig.get_python_inc())


for prefix in map(pathlib.Path,
                  [sysconfig.PREFIX,
                   sysconfig.EXEC_PREFIX,
                   sysconfig.BASE_PREFIX,
                   sysconfig.BASE_EXEC_PREFIX,
                   ]):
    assert prefix.exists()
    # print(prefix)


# with open(sysconfig.get_config_h_filename()) as fp:
#     pprint(sysconfig.parse_config_h(fp))
#
# pprint(sysconfig.get_config_vars())


def _load_header(header: pathlib.Path) -> dict:
    with open(header) as fp:
        return sysconfig.parse_config_h(fp)


def _load_headers() -> typing.Iterator[dict[pathlib.Path, dict]]:
    for header in _find_headers(PY_INCLUDE):
        yield (header, _load_header(header))


def _find_headers(src: pathlib.Path) -> typing.Iterator:
    for path in src.iterdir():
        if path.is_dir():
            yield from _find_headers(path)
        else:
            assert path.is_file()
            if path.suffix == '.h':
                yield path


def _find_python_install_info() -> typing.Iterator[dict]:
    yield from yaml.safe_load_all(
        subprocess.getoutput('{0} {1}'.format(
            command := pathlib.Path(__file__).with_name('generate_sources.sh'),
            command.with_name('data'),
            )))


if __name__ == '__main__':
    for header, dct in _load_headers():
        print(header.resolve())
        pprint(dct)
        print()

    for document in _find_python_install_info():
        path = pathlib.Path(CELLAR, document['formula'], document['keg'])
        assert path.exists()
        print(path)

        for header, exports in document['headers'].items():
            header = pathlib.Path(path,
                                   'Frameworks', 'Python.framework',
                                   'Headers', header,
                                   )
            assert header.exists()
            # pprint(_load_header(header))
            for symbol in exports:
                try:
                    tp = PyTypeObject.in_dll(ctypes.pythonapi, symbol)
                    # print(tp)
                except ValueError as exc:
                    print(f'{header}: {exc}')
