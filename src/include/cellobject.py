__all__ = [
    'PyCellObject', 'PyCellObject_p',
]


import ctypes


###


from .object import PyObject_HEAD


class PyCellObject(ctypes.Structure):
    """
    PyObject_HEAD
    PyObject *ob_ref;
    """

    _fields_ = [
        *PyObject_HEAD,
        # Content of the cell or NULL when empty
        ('ob_ref' , ctypes.py_object ),
    ]


PyCellObject_p = ctypes.POINTER(PyCellObject)
