__all__ = [
    'PyFloatObject', 'PyFloatObject_p',
]


import ctypes


###


from .object import PyObject_HEAD


class PyFloatObject(ctypes.Structure):
    """
    PyObject_HEAD
    double ob_fval;
    """

    _anonymous_ = ('ob_base',)
    _fields_ = [
        *PyObject_HEAD,
        ('ob_fval' , ctypes.c_double ),
    ]


PyFloatObject_p = ctypes.POINTER(PyFloatObject)
