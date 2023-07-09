__all__ = [
    'PyMethodObject', 'PyMethodObject_p',
    'PyInstanceMethodObject', 'PyInstanceMethodObject_p',
]


import ctypes

from .object import PyObject_HEAD


###


from .cpython.object import vectorcallfunc


class PyMethodObject(ctypes.Structure):
    """
    PyObject_HEAD
    PyObject *im_func;
    PyObject *im_self;
    PyObject *im_weakreflist;
    vectorcallfunc vectorcall;
    """

    _fields_ = [
        *PyObject_HEAD,
        # The callable object implementing the method
        ('im_func'        , ctypes.py_object ),
        # The instance it is bound to
        ('im_self'        , ctypes.py_object ),
        # List of weak references
        ('im_weakreflist' , ctypes.py_object ),
        ('vectorcall'     , vectorcallfunc   ),
    ]


PyMethodObject_p = ctypes.POINTER(PyMethodObject)


###


class PyInstanceMethodObject(ctypes.Structure):
    """
    PyObject_HEAD
    PyObject *func;
    """

    _fields_ = [
        *PyObject_HEAD,
        ('func' , ctypes.py_object ),
    ]


PyInstanceMethodObject_p = ctypes.POINTER(PyInstanceMethodObject)
