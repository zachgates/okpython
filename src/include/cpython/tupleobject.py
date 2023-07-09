__all__ = [
    'PyTupleObject', 'PyTupleObject_p',
    '_PyTuple_CAST',
    'PyTuple_GET_SIZE', 'PyTuple_GET_ITEM', 'PyTuple_SET_ITEM',
]


import ctypes

from ... import PyAPI_FUNC
from ..object import PyObject_p


###


from ..object import PyObject_VAR_HEAD


class PyTupleObject(ctypes.Structure):
    """
    PyObject_VAR_HEAD
    PyObject *ob_item[1];
    """

    # ob_item contains space for 'ob_size' elements.
    # Items must normally not be NULL, except during construction when
    # the tuple is not yet visible outside the function that builds it.

    _anonymous_ = ('ob_base',)
    _fields_ = [
        *PyObject_VAR_HEAD,
        ('_ob_item' , PyObject_p ),
    ]

    @property
    def ob_item(self):
        address = ctypes.addressof(self._ob_item)
        arr_t = ctypes.ARRAY(ctypes.py_object, self.ob_size)
        return arr_t.from_address(address)


PyTupleObject_p = ctypes.POINTER(PyTupleObject)


###


from ..object import PyObject_pp


PyAPI_FUNC("_PyTuple_Resize",
    restype = ctypes.c_int,
    argtypes = [
        PyObject_pp,
        ctypes.py_ssize_t,
    ])

PyAPI_FUNC("_PyTuple_MaybeUntrack",
    argtypes = [
        PyObject_p,
    ])


###


from ..object import Py_SIZE
from ..tupleobject import PyTuple_Check


# Cast argument to PyTupleObject* type.
def _PyTuple_CAST(op):
    """
    #define _PyTuple_CAST(op) (assert(PyTuple_Check(op)), (PyTupleObject *)(op))
    """
    assert PyTuple_Check(op)
    op = ctypes.cast(ctypes.byref(op), PyTupleObject_p)
    return op.contents


def PyTuple_GET_SIZE(op):
    """
    #define PyTuple_GET_SIZE(op)    Py_SIZE(_PyTuple_CAST(op))
    """
    return Py_SIZE(_PyTuple_CAST(op))


def PyTuple_GET_ITEM(op, i):
    """
    #define PyTuple_GET_ITEM(op, i) (_PyTuple_CAST(op)->ob_item[i])
    """
    return _PyTuple_CAST(op).ob_item[i]


# Macro, *only* to be used to fill in brand new tuples
def PyTuple_SET_ITEM(op, i, v):
    """
    #define PyTuple_SET_ITEM(op, i, v) (_PyTuple_CAST(op)->ob_item[i] = v)
    """
    _PyTuple_CAST(op).ob_item[i] = v


###


PyAPI_FUNC("_PyTuple_DebugMallocStats",
    argtypes = [
        ctypes.c_void_p, # FILE *
    ])
