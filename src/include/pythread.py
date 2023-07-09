__all__ = [
    'PyThread_type_lock', 'PyThread_type_lock_p',
    'Py_tss_t', 'Py_tss_t_p',
]


import ctypes


###


PyThread_type_lock = ctypes.c_void_p
PyThread_type_lock_p = ctypes.POINTER(PyThread_type_lock)


###


class Py_tss_t(ctypes.Structure):
    """
    int _is_initialized;
    NATIVE_TSS_KEY_T _key;
    """

    _fields_ = [
        ('_is_initialized' , ctypes.c_int   ),
        ('_key'            , ctypes.c_ulong ), # NATIVE_TSS_KEY_T
    ]


Py_tss_t_p = ctypes.POINTER(Py_tss_t)
