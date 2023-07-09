__all__ = [
    'Py_AuditHookFunction',
]


import ctypes

from ... import PyAPI_FUNC


###


from ..object import PyObject_p
from .object import _Py_Identifier_p


PyAPI_FUNC("_PySys_GetObjectId",
    restype = PyObject_p,
    argtypes = [
        _Py_Identifier_p,
    ])

PyAPI_FUNC("_PySys_SetObjectId",
    restype = ctypes.c_int,
    argtypes = [
        _Py_Identifier_p,
        PyObject_p,
    ])

PyAPI_FUNC("_PySys_GetSizeOf",
    restype = ctypes.c_size_t,
    argtypes = [
        PyObject_p,
    ])


###


Py_AuditHookFunction = ctypes.CFUNCTYPE(
    ctypes.c_int,
    ctypes.c_char_p, ctypes.py_object, ctypes.c_void_p,
    )


###


PyAPI_FUNC("PySys_Audit",
    restype = ctypes.c_int,
    argtypes = [
        ctypes.c_char_p,
        ctypes.c_char_p,
    ])

PyAPI_FUNC("PySys_AddAuditHook",
    restype = ctypes.c_int,
    argtypes = [
        Py_AuditHookFunction,
        ctypes.c_void_p,
    ])
