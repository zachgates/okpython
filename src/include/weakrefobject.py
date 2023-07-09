__all__ = [
    'PyWeakReference', 'PyWeakReference_p',
]


import ctypes


###


from .object import PyObject_HEAD


class PyWeakReference(ctypes.Structure):
    """
    PyObject_HEAD
    PyObject *wr_object;
    PyObject *wr_callback;
    Py_hash_t hash;
    PyWeakReference *wr_prev;
    PyWeakReference *wr_next;
    """

    # PyWeakReference is the base struct for the Python ReferenceType,
    # ProxyType, and CallableProxyType.

    _anonymous_ = ('ob_base',)


PyWeakReference_p = ctypes.POINTER(PyWeakReference)
PyWeakReference._fields_ = [
    *PyObject_HEAD,
    ('wr_object'   , ctypes.py_object  ),
    ('wr_callback' , ctypes.py_object  ),
    ('hash'        , ctypes.py_hash_t  ),
    ('wr_prev'     , PyWeakReference_p ),
    ('wr_next'     , PyWeakReference_p ),
]
