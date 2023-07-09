__all__ = [
    'PyByteArray_Type', 'PyByteArrayIter_Type',
    'PyByteArray_Check', 'PyByteArray_CheckExact',
    'PyByteArray_FromObject', 'PyByteArray_Concat',
    'PyByteArray_FromStringAndSize', 'PyByteArray_Size',
    'PyByteArray_AsString', 'PyByteArray_Resize',
]


import ctypes

from .. import PyAPI_DATA, PyAPI_FUNC


###


from .object import PyTypeObject


PyAPI_DATA("PyByteArray_Type",
    dtype = PyTypeObject,
    )

PyAPI_DATA("PyByteArrayIter_Type",
    dtype = PyTypeObject,
    )


###


from .object import Py_IS_TYPE, PyObject_TypeCheck


def PyByteArray_Check(self):
    """
    #define PyByteArray_Check(self) PyObject_TypeCheck(self, &PyByteArray_Type)
    """
    return PyObject_TypeCheck(self, PyByteArray_Type)


def PyByteArray_CheckExact(self):
    """
    #define PyByteArray_CheckExact(self) Py_IS_TYPE(self, &PyByteArray_Type)
    """
    return Py_IS_TYPE(self, PyByteArray_Type)


###


from .object import PyObject_p


PyAPI_FUNC("PyByteArray_FromObject",
    restype = PyObject_p,
    argtypes = [
        PyObject_p,
    ])

PyAPI_FUNC("PyByteArray_Concat",
    restype = PyObject_p,
    argtypes = [
        PyObject_p,
        PyObject_p,
    ])

PyAPI_FUNC("PyByteArray_FromStringAndSize",
    restype = PyObject_p,
    argtypes = [
        ctypes.c_char_p,
        ctypes.py_ssize_t,
    ])

PyAPI_FUNC("PyByteArray_Size",
    restype = ctypes.py_ssize_t,
    argtypes = [
        PyObject_p,
    ])

PyAPI_FUNC("PyByteArray_AsString",
    restype = ctypes.c_char_p,
    argtypes = [
        PyObject_p,
    ])

PyAPI_FUNC("PyByteArray_Resize",
    restype = ctypes.c_int,
    argtypes = [
        PyObject_p,
        ctypes.py_ssize_t,
    ])
