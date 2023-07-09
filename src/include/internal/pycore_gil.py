__all__ = [
    '_gil_runtime_state', '_gil_runtime_state_p',
]


import ctypes


###


from .pycore_atomic import _Py_atomic_address, _Py_atomic_int


class _gil_runtime_state(ctypes.Structure):
    """
    unsigned long interval;
    _Py_atomic_address last_holder;
    _Py_atomic_int locked;
    unsigned long switch_number;
    PyCOND_T cond;
    PyMUTEX_T mutex;
#ifdef FORCE_SWITCHING
    PyCOND_T switch_cond;
    PyMUTEX_T switch_mutex;
#endif
    """

    _fields_ = [
        ('interval'      , ctypes.c_ulong     ),
        ('last_holder'   , _Py_atomic_address ),
        ('locked'        , _Py_atomic_int     ),
        ('switch_number' , ctypes.c_ulong     ),
        # ('cond'          , PyCOND_T           ),
        # ('mutex'         , PyMUTEX_T          ),
        # ('switch_cond'   , PyCOND_T           ),
        # ('switch_mutex'  , PyMUTEX_T          ),
    ]


_gil_runtime_state_p = ctypes.POINTER(_gil_runtime_state)
