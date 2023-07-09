__all__ = [
    'PyCapsule', 'PyCapsule_p',
]


import ctypes


###


from ..include.object import PyObject_HEAD
from ..include.pycapsule import PyCapsule_Destructor


class PyCapsule(ctypes.Structure):
    """
    PyObject_HEAD
    void *pointer;
    const char *name;
    void *context;
    PyCapsule_Destructor destructor;
    """

    _fields_ = [
        *PyObject_HEAD,
        ('pointer'    , ctypes.c_void_p      ),
        ('name'       , ctypes.c_char_p      ),
        ('context'    , ctypes.c_void_p      ),
        ('destructor' , PyCapsule_Destructor ),
    ]


PyCapsule_p = ctypes.POINTER(PyCapsule)
