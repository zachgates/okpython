__all__ = [
    'PySliceObject', 'PySliceObject_p',
]


import ctypes


###


from .object import PyObject_HEAD


class PySliceObject(ctypes.Structure):
    """
    PyObject_HEAD
    PyObject *start, *stop, *step;
    """

    # not NULL

    _fields_ = [
        *PyObject_HEAD,
        ('start' , ctypes.py_object ),
        ('stop'  , ctypes.py_object ),
        ('step'  , ctypes.py_object ),
    ]


PySliceObject_p = ctypes.POINTER(PySliceObject)
