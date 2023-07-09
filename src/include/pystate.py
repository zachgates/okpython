__all__ = [
    'MAX_CO_EXTRA_USERS',
    'PyInterpreterState', 'PyInterpreterState_p',
    'PyThreadState', 'PyThreadState_p',
]


import ctypes


###


# This limitation is for performance and simplicity. If needed it can be
# removed (with effort).
MAX_CO_EXTRA_USERS = 255


###


from .internal.pycore_interp import _is


class PyInterpreterState(ctypes.Structure): # _is
    _anonymous_ = ('_',)
    _fields_ = [
        ('_' , _is )
    ]


PyInterpreterState_p = ctypes.POINTER(PyInterpreterState)


###


from .cpython.pystate import _ts


class PyThreadState(ctypes.Structure): # _ts
    _anonymous_ = ('_',)
    _fields_ = [
        ('_' , _ts )
    ]


PyThreadState_p = ctypes.POINTER(PyThreadState)
