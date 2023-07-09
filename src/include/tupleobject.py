"""
Another generally useful object type is a tuple of object pointers.
For Python, this is an immutable type.  C code can change the tuple items
(but not their number), and even use tuples as general-purpose arrays of
object references, but in general only brand new tuples should be mutated,
not ones that might already have been exposed to Python code.

*** WARNING *** PyTuple_SetItem does not increment the new item's reference
count, but does decrement the reference count of the item it replaces,
if not nil.  It does *decrement* the reference count if it is *not*
inserted in the tuple.  Similarly, PyTuple_GetItem does not increment the
returned item's reference count.
"""

__all__ = [
    'PyTuple_Check', 'PyTuple_CheckExact',
]


import ctypes

from .. import PyAPI_DATA, PyAPI_FUNC


###


from .object import PyTypeObject


PyAPI_DATA("PyTuple_Type",
    dtype = PyTypeObject,
    )

PyAPI_DATA("PyTupleIter_Type",
    dtype = PyTypeObject,
    )


###


from .object import Py_TYPE, Py_IS_TYPE, PyType_FastSubclass, TPFLAG


def PyTuple_Check(op):
    """
    #define PyTuple_Check(op) \
                     PyType_FastSubclass(Py_TYPE(op), Py_TPFLAGS_TUPLE_SUBCLASS)
    """
    return PyType_FastSubclass(Py_TYPE(op), TPFLAG('TUPLE_SUBCLASS'))


def PyTuple_CheckExact(op):
    """
    #define PyTuple_CheckExact(op) Py_IS_TYPE(op, &PyTuple_Type)
    """
    return Py_IS_TYPE(op, PyTuple_Type)


###


from .object import PyObject_p


PyAPI_FUNC("PyTuple_New",
    restype = PyObject_p,
    argtypes = [
        ctypes.py_ssize_t, # size
    ])

PyAPI_FUNC("PyTuple_Size",
    restype = ctypes.py_ssize_t,
    argtypes = [
        PyObject_p,
    ])

PyAPI_FUNC("PyTuple_GetItem",
    restype = PyObject_p,
    argtypes = [
        PyObject_p,
        ctypes.py_ssize_t,
    ])

PyAPI_FUNC("PyTuple_SetItem",
    restype = ctypes.c_int,
    argtypes = [
        PyObject_p,
        ctypes.py_ssize_t,
        PyObject_p,
    ])

PyAPI_FUNC("PyTuple_GetSlice",
    restype = PyObject_p,
    argtypes = [
        PyObject_p,
        ctypes.py_ssize_t,
        ctypes.py_ssize_t,
    ])

PyAPI_FUNC("PyTuple_Pack",
    restype = PyObject_p,
    argtypes = [
        ctypes.py_ssize_t,
        # ...
    ])
