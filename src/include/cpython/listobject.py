__all__ = [
    'PyListObject', 'PyListObject_p',
]


import ctypes

from ..object import PyObject_p


###


from ..object import PyObject_VAR_HEAD


class PyListObject(ctypes.Structure):
    """
    PyObject_VAR_HEAD
    PyObject **ob_item;
    Py_ssize_t allocated;
    """

    # ob_item contains space for 'allocated' elements.
    # The number currently in use is ob_size.
    #
    # Invariants:
    #   - 0 <= ob_size <= allocated
    #   - len(list) == ob_size
    #   - ob_item == NULL implies ob_size == allocated == 0
    #
    # list.sort() temporarily sets allocated to -1 to detect mutations.
    #
    # Items must normally not be NULL, except during construction when
    # the list is not yet visible outside the function that builds it.

    _anonymous_ = ('ob_base',)
    _fields_ = [
        *PyObject_VAR_HEAD,
        # Vector of pointers to list elements.  list[0] is ob_item[0], etc.
        ('_ob_item'  , ctypes.POINTER(PyObject_p) ),
        ('allocated' , ctypes.py_ssize_t          ),
    ]

    def ob_item(self, index):
        if index >= self.ob_size:
            raise IndexError('invalid index')
        else:
            return self._ob_item[index]


PyListObject_p = ctypes.POINTER(PyListObject)


###


from ... import PyAPI_FUNC


PyAPI_FUNC("_PyList_Extend",
    restype = PyObject_p,
    argtypes = [
        PyListObject_p,
        PyObject_p,
    ])

PyAPI_FUNC("_PyList_DebugMallocStats",
    argtypes = [
        ctypes.c_void_p, # FILE *
    ])
