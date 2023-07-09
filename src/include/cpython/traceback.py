__all__ = [
    'PyTracebackObject', 'PyTracebackObject_p',
]


import ctypes


###


from ..object import PyObject_HEAD
from ..pyframe import PyFrameObject_p


class PyTracebackObject(ctypes.Structure):
    """
    PyObject_HEAD
    struct _traceback *tb_next;
    PyFrameObject *tb_frame;
    int tb_lasti;
    int tb_lineno;
    """


PyTracebackObject_p = ctypes.POINTER(PyTracebackObject)
PyTracebackObject._fields_ = [
    *PyObject_HEAD,
    ('tb_next'   , PyTracebackObject_p ),
    ('tb_frame'  , PyFrameObject_p     ),
    ('tb_lasti'  , ctypes.c_int        ),
    ('tb_lineno' , ctypes.c_int        ),
]


###


from ... import PyAPI_FUNC
from ..object import PyObject_p


PyAPI_FUNC("_Py_DisplaySourceLine",
    restype = ctypes.c_int,
    argtypes = [
        PyObject_p,
        PyObject_p,
        ctypes.c_int,
        ctypes.c_int,
    ])

PyAPI_FUNC("_PyTraceback_Add",
    argtypes = [
        ctypes.c_char_p,
        ctypes.c_char_p,
        ctypes.c_int,
    ])
