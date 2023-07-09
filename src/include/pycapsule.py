__all__ = [
    'PyCapsule_Destructor',
]


import ctypes


###


PyCapsule_Destructor = ctypes.CFUNCTYPE(
    None,
    ctypes.py_object,
    )
