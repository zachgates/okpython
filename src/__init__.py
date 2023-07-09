__all__ = [
    'PyTypeObject', 'PyTypeObject_p',
    'PyObject', 'PyObject_p',
    'PyVarObject', 'PyVarObject_p',
]

import ctypes
import functools
import struct
import sys
import types


ctypes.abi = types.SimpleNamespace()
ctypes.pythonapi._FuncPtr.__repr__ = lambda self: \
    f'<{self.__class__.__name__} {self.__name__!s} at 0x{id(self):x}>'


ctypes.py_ssize_t = (
    ctypes.c_size_t
    if sys.version_info > (2, 4)
    else ctypes.c_int
    )


ctypes.py_hash_t = (
    ctypes.c_int64
    if (8 * struct.calcsize('P') == 64) # __LP64__
    else ctypes.c_int32
    )


def reframe(func):
    @functools.wraps(func)
    def wrapper(name, **kwargs):
        value = func(name, **kwargs)
        frame = sys._getframe(1)
        frame.f_globals[name] = value
        frame.f_globals['__all__'].append(name)
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


class PyTypeObject(ctypes.Structure):
    ...


class PyObject(ctypes.Structure):
    _fields_ = [
        ( 'ob_refcnt' , ctypes.c_size_t  ),
        ( 'ob_type'   , ctypes.py_object ),
    ]


class PyVarObject(ctypes.Structure):
    _anonymous_ = ('ob_base',)
    _fields_ = [
        ( 'ob_base' , PyObject         ),
        ( 'ob_size' , ctypes.py_hash_t ),
    ]


PyTypeObject._anonymous_ = ('ob_base',)
PyTypeObject._fields_ = [
    ( 'ob_base' , PyVarObject     ),
    ( 'tp_name' , ctypes.c_char_p ),
]


PyTypeObject_p = ctypes.POINTER(PyTypeObject)
PyObject_p = ctypes.POINTER(PyObject)
PyVarObject_p = ctypes.POINTER(PyVarObject)
