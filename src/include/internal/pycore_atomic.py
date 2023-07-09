__all__ = [
    '_Py_atomic_address', '_Py_atomic_address_p',
    '_Py_atomic_int', '_Py_atomic_int_p',
]


import ctypes


###


class _Py_atomic_address(ctypes.Structure):
    """
    uintptr_t _value;
    """

    _fields_ = [
        ('_value' , ctypes.c_void_p ),
    ]


_Py_atomic_address_p = ctypes.POINTER(_Py_atomic_address)


###


class _Py_atomic_int(ctypes.Structure):
    """
    int _value;
    """

    _fields_ = [
        ('_value' , ctypes.c_int ),
    ]


_Py_atomic_int_p = ctypes.POINTER(_Py_atomic_int)
