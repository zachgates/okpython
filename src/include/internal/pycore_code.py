__all__ = [
    '_PyOpcache_LoadGlobal', '_PyOpcache_LoadGlobal_p',
    '_PyOpcache', '_PyOpcache_p',
]


import ctypes


###


class _PyOpcache_LoadGlobal(ctypes.Structure):
    """
    PyObject *ptr;
    uint64_t globals_ver;
    uint64_t builtins_ver;
    """

    _fields_ = [
        # Cached pointer (borrowed reference)
        ('ptr'          , ctypes.py_object ),
        # ma_version of global dict
        ('globals_ver'  , ctypes.c_uint64  ),
        # ma_version of builtin dict
        ('builtins_ver' , ctypes.c_uint64  ),
    ]


_PyOpcache_LoadGlobal_p = ctypes.POINTER(_PyOpcache_LoadGlobal)


###


class _PyOpcache(ctypes.Structure):
    """
    union {
        _PyOpcache_LoadGlobal lg;
    } u;
    char optimized;
    """

    class u(ctypes.Union):
        _fields_ = [
            ('lg' , _PyOpcache_LoadGlobal ),
        ]

    _fields_ = [
        ('u'         , u             ),
        ('optimized' , ctypes.c_char ),
    ]


_PyOpcache_p = ctypes.POINTER(_PyOpcache)
