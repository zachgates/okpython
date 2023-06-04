__all__ = [
    'PyTypeObject', 'PyTypeObject_p',
    'PyObject', 'PyObject_p',
    'PyVarObject', 'PyVarObject_p',
]

import ctypes
import struct
import sys


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
