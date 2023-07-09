__all__ = [
    'PyModuleObject', 'PyModuleObject_p',
]


import ctypes


###


from ..include.object import PyObject_HEAD, PyObject_p
from ..include.moduleobject import PyModuleDef_p


class PyModuleObject(ctypes.Structure):
    """
    PyObject_HEAD
    PyObject *md_dict;
    struct PyModuleDef *md_def;
    void *md_state;
    PyObject *md_weaklist;
    PyObject *md_name;
    """

    _fields_ = [
        *PyObject_HEAD,
        ('md_dict'     , PyObject_p      ),
        ('md_def'      , PyModuleDef_p   ),
        ('md_state'    , ctypes.c_void_p ),
        ('md_weaklist' , PyObject_p      ),
        ('md_name'     , PyObject_p      ),
    ]


PyModuleObject_p = ctypes.POINTER(PyModuleObject)
