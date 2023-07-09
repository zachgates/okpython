__all__ = [
    'PyByteArrayObject', 'PyByteArrayObject_p',
    'PyByteArray_AS_STRING', 'PyByteArray_GET_SIZE',
]


import ctypes

from ... import PyAPI_DATA


###


from ..object import PyObject_VAR_HEAD


class PyByteArrayObject(ctypes.Structure):
    """
    PyObject_VAR_HEAD
    Py_ssize_t ob_alloc;
    char *ob_bytes;
    char *ob_start;
    Py_ssize_t ob_exports;
    """

    _anonymous_ = ('ob_base',)
    _fields_ = [
        *PyObject_VAR_HEAD,

        # How many bytes allocated in ob_bytes
        ('ob_alloc'   , ctypes.py_ssize_t ),

        # Physical backing buffer
        ('ob_bytes'   , ctypes.c_char_p   ),

        # Logical start inside ob_bytes
        ('ob_start'   , ctypes.c_char_p   ),

        # How many buffer exports
        ('ob_exports' , ctypes.py_ssize_t ),
    ]


PyByteArrayObject_p = ctypes.POINTER(PyByteArrayObject)


###


from ..bytearrayobject import PyByteArray_Check
from ..object import Py_SIZE


def PyByteArray_AS_STRING(self):
    """
    #define PyByteArray_AS_STRING(self) \
        (assert(PyByteArray_Check(self)), \
         Py_SIZE(self) ? ((PyByteArrayObject *)(self))->ob_start : _PyByteArray_empty_string)
    """
    assert PyByteArray_Check(self)

    if Py_SIZE(self):
        self = ctypes.cast(ctypes.byref(self), PyByteArrayObject_p)
        return self.contents.ob_start
    else:
        return _PyByteArray_empty_string


def PyByteArray_GET_SIZE(self):
    """
    #define PyByteArray_GET_SIZE(self) (assert(PyByteArray_Check(self)), Py_SIZE(self))
    """
    assert PyByteArray_Check(self)
    return Py_SIZE(self)


###


PyAPI_DATA("_PyByteArray_empty_string",
    dtype = ctypes.ARRAY(ctypes.c_char, 0),
	)
