__all__ = [
    '_Py_MANAGED_BUFFER_RELEASED', '_Py_MANAGED_BUFFER_FREE_FORMAT',
    '_PyManagedBufferObject', '_PyManagedBufferObject_p',
    '_MEMORYVIEW', 'PyMemoryViewObject', 'PyMemoryViewObject_p',
]


import ctypes


###


from .object import PyObject_HEAD
from .cpython.object import Py_buffer


_Py_MANAGED_BUFFER_RELEASED    = 0x001
_Py_MANAGED_BUFFER_FREE_FORMAT = 0x002


class _PyManagedBufferObject(ctypes.Structure):
    """
    PyObject_HEAD
    int flags;
    Py_ssize_t exports;
    Py_buffer master;
    """

    _anonymous_ = ('ob_base',)
    _fields_ = [
        *PyObject_HEAD,
        # state flags
        ('flags'   , ctypes.c_int      ),
        # number of direct memoryview exports
        ('exports' , ctypes.py_ssize_t ),
        # snapshot buffer obtained from the original exporter
        ('master'  , Py_buffer         ),
    ]


_PyManagedBufferObject_p = ctypes.POINTER(_PyManagedBufferObject)


###


from .. import FlagGroup


class _MEMORYVIEW(FlagGroup):
    """
    memoryview state flags
    """

    def __str__(self):
        return f'_Py_{self.__class__.__name__}_{self._name_}'

    RELEASED = (1 << 0) # access to master buffer blocked
    C        = (1 << 1) # C-contiguous layout
    FORTRAN  = (1 << 2) # Fortran contiguous layout
    SCALAR   = (1 << 3) # scalar: ndim = 0
    PIL      = (1 << 4) # PIL-style layout


###


from .object import PyObject_VAR_HEAD


class PyMemoryViewObject(ctypes.Structure):
    """
    PyObject_VAR_HEAD
    _PyManagedBufferObject *mbuf;
    Py_hash_t hash;
    int flags;
    Py_ssize_t exports;
    Py_buffer view;
    PyObject *weakreflist;
    Py_ssize_t ob_array[1];
    """

    _anonymous_ = ('ob_base',)
    _fields_ = [
        *PyObject_VAR_HEAD,
        # managed buffer
        ('mbuf'        , _PyManagedBufferObject_p ),
        # hash value for read-only views
        ('hash'        , ctypes.py_hash_t         ),
        # state flags
        ('flags'       , ctypes.c_int             ),
        # number of buffer re-exports
        ('exports'     , ctypes.py_ssize_t        ),
        # private copy of the exporter's view
        ('view'        , Py_buffer                ),
        ('weakreflist' , ctypes.py_object         ),
        # shape, strides, suboffsets
        ('ob_array'    , ctypes.py_ssize_t        ),
    ]


PyMemoryViewObject_p = ctypes.POINTER(PyMemoryViewObject)
