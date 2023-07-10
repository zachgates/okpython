__all__ = []


###


import enum


class HookExt(enum.EnumMeta):

    def hook_contents(cls, dct: dict, *, soft: bool = False):
        if soft:
            for member in cls:
                dct.setdefault(str(member), member.value)
        else:
            dct.update({str(member): member.value for member in cls})


class Flag(enum.Enum):

    def __repr__(self):
        return f'<{str(self)}: {int(self)}>'

    def __int__(self):
        return self.value

    def __eq__(self, other):
        return (int(self) == int(other))

    def __or__(self, other):
        return (int(self) | int(other))

    __ror__ = __or__
    __add__ = __radd__ = __or__

    def __and__(self, other):
        return (int(self) & other)

    __rand__ = __and__

    def __reduce_ex__(self, proto):
        return super().__str__()


class FlagGroup(HookExt):

    def __call__(self, *args, **kwargs):
        raise TypeError(f'{self.__name__!r} object is not callable')

    def __getitem__(self, name: str):
        if isinstance(name, str):
            return getattr(self, name.upper(), self.NONE)
        else:
            raise TypeError('a string is required for flag name')

    def _select(self, name):
        if name is None:
            return self.NONE
        else:
            return self[name]


class FlagGroup(Flag, metaclass = FlagGroup):
    pass


class MacroFactoryGroup(HookExt):

    def __call__(self, name: str, **kwargs):
        if not isinstance(name, str):
            raise TypeError('a string is required (got type %s)'
                            % type(name).__name__)

        if 'value' in kwargs:
            value = kwargs.pop('value')
            other = kwargs.pop('other', None)
            return self[name:value:other]
        else:
            return self[name]

    def __getitem__(self, value: str):
        if isinstance(value, str):
            return getattr(self, value)
        elif isinstance(value, slice):
            try:
                factory = getattr(self, value.start)
            except AttributeError as exc:
                if value.step is Ellipsis:
                    return None
                else:
                    raise exc
            else:
                try:
                    # if (value.stop is None) and (value.step is None):
                    #     return factory()
                    return factory(value.stop)
                except TypeError as exc:
                    if value.step is Ellipsis:
                        return None
                    elif value.step is None:
                        raise exc
                    else:
                        return factory(value.step)
        else:
            raise TypeError('a string or slice is required (got type %s)'
                            % type(value).__name__)


###


import ctypes
import functools
import sys
import types


ctypes.abi = types.SimpleNamespace()
ctypes.pythonapi._FuncPtr.__repr__ = lambda self: \
    f'<{self.__class__.__name__} {self.__name__} at 0x{id(self):x}>'


def reframe(func):
    @functools.wraps(func)
    def wrapper(symbol, **kwargs):
        value = func(symbol, **kwargs)
        frame = sys._getframe(1)
        frame.f_globals[symbol] = value
        frame.f_globals['__all__'].append(symbol)
        return value
    return wrapper


@reframe
def PyAPI_DATA(symbol, *, dtype):
    return dtype.in_dll(ctypes.pythonapi, symbol)


@reframe
def PyAPI_FUNC(name, *, restype = None, argtypes = None):
    setattr(ctypes.abi, name, func := ctypes.pythonapi[name])
    func.restype = restype
    func.argtypes = argtypes
    return func


###


import importlib


_modules = [
    '.objects.capsule',
    '.objects.dict_common',
    '.objects.dictobject',
    '.objects.moduleobject',
    '.objects.odictobject',
    #
    '.include.bytesobject',
    '.include.bytearrayobject',
    '.include.cellobject',
    '.include.classobject',
    '.include.compile',
    '.include.complexobject',
    '.include.context',
    '.include.descrobject',
    '.include.dictobject',
    '.include.floatobject',
    '.include.funcobject',
    '.include.genobject',
    '.include.longintrepr',
    '.include.memoryobject',
    '.include.methodobject',
    '.include.modsupport',
    '.include.moduleobject',
    '.include.object',
    '.include.odictobject',
    '.include.pycapsule',
    '.include.pyframe',
    '.include.pyport',
    '.include.pystate',
    '.include.pythread',
    '.include.setobject',
    '.include.sliceobject',
    '.include.structmember',
    '.include.structseq',
    '.include.tupleobject',
    '.include.typeslots',
    '.include.weakrefobject',
    #
    '.include.cpython.bytearrayobject',
    '.include.cpython.bytesobject',
    '.include.cpython.code',
    '.include.cpython.dictobject',
    '.include.cpython.fileobject',
    '.include.cpython.fileutils',
    '.include.cpython.frameobject',
    '.include.cpython.initconfig',
    '.include.cpython.listobject',
    '.include.cpython.object',
    '.include.cpython.pystate',
    '.include.cpython.sysmodule',
    '.include.cpython.traceback',
    '.include.cpython.tupleobject',
    #
    '.include.internal.pycore_atomic',
    '.include.internal.pycore_code',
    '.include.internal.pycore_context',
    '.include.internal.pycore_gc',
    '.include.internal.pycore_gil',
    '.include.internal.pycore_hamt',
    '.include.internal.pycore_initconfig',
    '.include.internal.pycore_interp',
    '.include.internal.pycore_runtime',
    '.include.internal.pycore_warnings',
]


for _module in _modules:
    _module = importlib.import_module(_module, __package__)
    __all__.extend(_module.__all__)
    for _name in _module.__all__:
        _object = getattr(_module, _name)
        setattr(ctypes.abi, _name, _object)
        globals()[_name] = _object
