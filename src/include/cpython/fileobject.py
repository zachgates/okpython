__all__ = [
    'Py_OpenCodeHookFunction',
]


import ctypes

from ... import PyAPI_DATA, PyAPI_FUNC
from ..object import PyObject_p


###


from ..object import PyTypeObject


PyAPI_FUNC("Py_UniversalNewlineFgets",
    restype = ctypes.c_char_p,
    argtypes = [
        ctypes.c_char_p,
        ctypes.c_int,
        ctypes.c_void_p, # FILE *
        PyObject_p,
    ])

# The std printer acts as a preliminary sys.stderr until the new io
# infrastructure is in place.
PyAPI_FUNC("PyFile_NewStdPrinter",
    restype = PyObject_p,
    argtypes = [
        ctypes.c_int,
    ])

PyAPI_DATA("PyStdPrinter_Type",
    dtype = PyTypeObject,
    )


###


Py_OpenCodeHookFunction = ctypes.CFUNCTYPE(
    ctypes.py_object,
    ctypes.py_object, ctypes.c_void_p,
    )


###


PyAPI_FUNC("PyFile_OpenCode",
    restype = PyObject_p,
    argtypes = [
        ctypes.c_char_p, # utf8path
    ])

PyAPI_FUNC("PyFile_OpenCodeObject",
    restype = PyObject_p,
    argtypes = [
        PyObject_p, # path
    ])

PyAPI_FUNC("PyFile_SetOpenCodeHook",
    restype = ctypes.c_int,
    argtypes = [
        Py_OpenCodeHookFunction, # hook
        ctypes.c_void_p,         # userData
    ])
