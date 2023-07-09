"""
Type PyBytesObject represents a character string.  An extra zero byte is
reserved at the end to ensure it is zero-terminated, but a size is
present so strings with null bytes in them can be represented.  This
is an immutable object type.

There are functions to create new string objects, to test
an object for string-ness, and to get the
string value.  The latter function returns a null pointer
if the object is not of the proper type.
There is a variant that takes an explicit size as well as a
variant that assumes a zero-terminated string.  Note that none of the
functions should be applied to nil objects.
"""

__all__ = [
    'PyBytes_Type', 'PyBytesIter_Type',
    'PyBytes_Check', 'PyBytes_CheckExact',
    'F_LJUST', 'F_SIGN', 'F_BLANK', 'F_ALT', 'F_ZERO',
]


import ctypes

from .. import PyAPI_DATA, PyAPI_FUNC


###


from .object import PyTypeObject


PyAPI_DATA("PyBytes_Type",
    dtype = PyTypeObject,
    )

PyAPI_DATA("PyBytesIter_Type",
    dtype = PyTypeObject,
    )


###


from .object import Py_TYPE, Py_IS_TYPE, TPFLAG, PyType_FastSubclass


def PyBytes_Check(op):
    """
    #define PyBytes_Check(op) \
                     PyType_FastSubclass(Py_TYPE(op), Py_TPFLAGS_BYTES_SUBCLASS)
    """
    return PyType_FastSubclass(Py_TYPE(op), TPFLAG('BYTES_SUBCLASS'))


def PyBytes_CheckExact(op):
    """
    #define PyBytes_CheckExact(op) Py_IS_TYPE(op, &PyBytes_Type)
    """
    return Py_IS_TYPE(op, PyBytes_Type)


###


from .object import PyObject_p, PyObject_pp


PyAPI_FUNC("PyBytes_FromStringAndSize",
    restype = PyObject_p,
    argtypes = [
        ctypes.c_char_p,
        ctypes.py_ssize_t,
    ])

PyAPI_FUNC("PyBytes_FromString",
    restype = PyObject_p,
    argtypes = [
        ctypes.c_char_p,
    ])

PyAPI_FUNC("PyBytes_FromObject",
    restype = PyObject_p,
    argtypes = [
        PyObject_p,
    ])

PyAPI_FUNC("PyBytes_FromFormatV",
    restype = PyObject_p,
    argtypes = [
        ctypes.c_char_p,
        ctypes.va_list,
    ])

PyAPI_FUNC("PyBytes_FromFormat",
    restype = PyObject_p,
    argtypes = [
        ctypes.c_char_p,
    ])

PyAPI_FUNC("PyBytes_Size",
    restype = ctypes.py_ssize_t,
    argtypes = [
        PyObject_p,
    ])

PyAPI_FUNC("PyBytes_AsString",
    restype = ctypes.c_char_p,
    argtypes = [
        PyObject_p,
    ])

PyAPI_FUNC("PyBytes_Repr",
    restype = PyObject_p,
    argtypes = [
        PyObject_p,
        ctypes.c_int,
    ])

PyAPI_FUNC("PyBytes_Concat",
    argtypes = [
        PyObject_pp,
        PyObject_p,
    ])

PyAPI_FUNC("PyBytes_ConcatAndDel",
    argtypes = [
        PyObject_pp,
        PyObject_p,
    ])

PyAPI_FUNC("PyBytes_DecodeEscape",
    restype = PyObject_p,
    argtypes = [
        ctypes.c_char_p,
        ctypes.py_ssize_t,
        ctypes.c_char_p,
        ctypes.py_ssize_t,
        ctypes.c_char_p,
    ])

# Provides access to the internal data buffer and size of a string
# object or the default encoded version of a Unicode object. Passing
# NULL as *len parameter will force the string buffer to be
# 0-terminated (passing a string with embedded NULL characters will
# cause an exception).
PyAPI_FUNC("PyBytes_AsStringAndSize",
    restype = ctypes.c_int,
    argtypes = [
        # string or Unicode object
        PyObject_p,        # obj
        # pointer to buffer variable
        ctypes.c_char_pp,  # s
        # pointer to length variable
        # or NULL (only possible for 0-terminated strings)
        ctypes.py_ssize_t, # len
    ])


### Flags used by string formatting


F_LJUST = ( 1 << 0 )
F_SIGN  = ( 1 << 1 )
F_BLANK = ( 1 << 2 )
F_ALT   = ( 1 << 3 )
F_ZERO  = ( 1 << 4 )
