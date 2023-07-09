__all__ = [
    '_warnings_runtime_state', '_warnings_runtime_state_p',
]


import ctypes


###


class _warnings_runtime_state(ctypes.Structure):
    """
    PyObject *filters;
    PyObject *once_registry;
    PyObject *default_action;
    long filters_version;
    """

    _fields_ = [
        ('filters'         , ctypes.py_object ),
        ('once_registry'   , ctypes.py_object ),
        ('default_action'  , ctypes.py_object ),
        ('filters_version' , ctypes.c_long    ),
    ]


_warnings_runtime_state_p = ctypes.POINTER(_warnings_runtime_state)
