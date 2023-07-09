__all__ = [
    '_pycontextobject', '_pycontextobject_p',
    '_pycontextvarobject', '_pycontextvarobject_p',
    '_pycontexttokenobject', '_pycontexttokenobject_p',
]


import ctypes

from ..object import PyObject_HEAD


###


from .pycore_hamt import PyHamtObject_p


class _pycontextobject(ctypes.Structure):
    """
    PyObject_HEAD
    PyContext *ctx_prev;
    PyHamtObject *ctx_vars;
    PyObject *ctx_weakreflist;
    int ctx_entered;
    """


_pycontextobject_p = ctypes.POINTER(_pycontextobject)
_pycontextobject._fields_ = [
    *PyObject_HEAD,
    ('ctx_prev'        , _pycontextobject_p ),
    ('ctx_vars'        , PyHamtObject_p     ),
    ('ctx_weakreflist' , ctypes.py_object   ),
    ('ctx_entered'     , ctypes.c_int       ),
]


###


class _pycontextvarobject(ctypes.Structure):
    """
    PyObject_HEAD
    PyObject *var_name;
    PyObject *var_default;
    PyObject *var_cached;
    uint64_t var_cached_tsid;
    uint64_t var_cached_tsver;
    Py_hash_t var_hash;
    """

    _fields_ = [
        *PyObject_HEAD,
        ('var_name'         , ctypes.py_object ),
        ('var_default'      , ctypes.py_object ),
        ('var_cached'       , ctypes.py_object ),
        ('var_cached_tsid'  , ctypes.c_uint64  ),
        ('var_cached_tsver' , ctypes.c_uint64  ),
        ('var_hash'         , ctypes.py_hash_t ),
    ]


_pycontextvarobject_p = ctypes.POINTER(_pycontextvarobject)


###


class _pycontexttokenobject(ctypes.Structure):
    """
    PyObject_HEAD
    PyContext *tok_ctx;
    PyContextVar *tok_var;
    PyObject *tok_oldval;
    int tok_used;
    """

    _fields_ = [
        *PyObject_HEAD,
        ('tok_ctx'    , _pycontextobject_p    ),
        ('tok_var'    , _pycontextvarobject_p ),
        ('tok_oldval' , ctypes.py_object      ),
        ('tok_used'   , ctypes.c_int          ),
    ]


_pycontexttokenobject_p = ctypes.POINTER(_pycontexttokenobject)
