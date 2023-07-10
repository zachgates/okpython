import dataclasses
import pathlib
import subprocess
import typing
import yaml


__file__ = pathlib.Path(__file__)
CELLAR = subprocess.getoutput('brew --cellar')


@dataclasses.dataclass
class PythonPackage(object):

    formula: str = dataclasses.field(default = '')
    keg: str = dataclasses.field(default = '')
    headers: dict = dataclasses.field(default_factory = dict)

    @property
    def path(self):
        return pathlib.Path(self.formula, self.keg)

    def get_source(self, header: str):
        return pathlib.Path(
            CELLAR, self.formula, self.keg,
            'Frameworks', 'Python.framework',
            'Versions', 'Current', 'Headers', header,
            )

    def get_cache(self, cache: pathlib.Path, header: str):
        return pathlib.Path(cache, self.formula, self.keg, header)


def find_python_packages() -> typing.Iterator[PythonPackage]:
    for document in yaml.safe_load_all(
        subprocess.getoutput('{0} {1}'.format(
            __file__.with_name('find_headers.sh'),
            __file__.with_name('data'),
            ))):
                yield PythonPackage(**document)
