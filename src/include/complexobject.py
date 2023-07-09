__all__ = [
    'Py_complex', 'Py_complex_p',
    'PyComplexObject', 'PyComplexObject_p',
]


import ctypes


###


class Py_complex(ctypes.Structure):
    """
    double real;
    double imag;
    """

    _fields_ = [
        ('real' , ctypes.c_double ),
        ('imag' , ctypes.c_double ),
    ]


Py_complex_p = ctypes.POINTER(Py_complex)


###


from .object import PyObject_HEAD


class PyComplexObject(ctypes.Structure):
    """
    PyObject_HEAD
    Py_complex cval;
    """

    # PyComplexObject represents a complex number with double-precision
    # real and imaginary parts.

    _anonymous_ = ('ob_base',)
    _fields_ = [
        *PyObject_HEAD,
        ('cval' , Py_complex ),
    ]


PyComplexObject_p = ctypes.POINTER(PyComplexObject)
