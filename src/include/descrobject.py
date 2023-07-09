__all__ = [
    'getter', 'setter', 'PyGetSetDef', 'PyGetSetDef_p',
    'wrapperfunc', 'wrapperfunc_kwds', 'wrapperbase', 'wrapperbase_p',
    'PyDescrObject', 'PyDescrObject_p', 'PyDescr_COMMON',
    'PyMethodDescrObject', 'PyMethodDescrObject_p',
    'PyMemberDescrObject', 'PyMemberDescrObject_p',
    'PyGetSetDescrObject', 'PyGetSetDescrObject_p',
    'PyWrapperDescrObject', 'PyWrapperDescrObject_p',
]


import ctypes


###


getter = ctypes.CFUNCTYPE(
    ctypes.py_object,
    ctypes.py_object, ctypes.c_void_p,
    )

setter = ctypes.CFUNCTYPE(
    ctypes.c_int,
    ctypes.py_object, ctypes.py_object, ctypes.c_void_p,
    )


class PyGetSetDef(ctypes.Structure):
    """
    const char *name;
    getter get;
    setter set;
    const char *doc;
    void *closure;
    """

    _fields_ = [
        ('name'    , ctypes.c_char_p  ),
        ('get'     , getter           ),
        ('set'     , setter           ),
        ('doc'     , ctypes.c_char_p  ),
        ('closure' , ctypes.c_void_p  ),
    ]


PyGetSetDef_p = ctypes.POINTER(PyGetSetDef)


###


wrapperfunc = ctypes.CFUNCTYPE(
    ctypes.py_object,
    ctypes.py_object, ctypes.py_object, ctypes.c_void_p,
    )

wrapperfunc_kwds = ctypes.CFUNCTYPE(
    ctypes.py_object,
    ctypes.py_object, ctypes.py_object, ctypes.c_void_p, ctypes.py_object,
    )


class wrapperbase(ctypes.Structure):
    """
    const char *name;
    int offset;
    void *function;
    wrapperfunc wrapper;
    const char *doc;
    int flags;
    PyObject *name_strobj;
    """

    _fields_ = [
        ('name'        , ctypes.c_char_p  ),
        ('offset'      , ctypes.c_int     ),
        ('function'    , ctypes.c_void_p  ),
        ('wrapper'     , wrapperfunc      ),
        ('doc'         , ctypes.c_void_p  ),
        ('flags'       , ctypes.c_int     ),
        ('name_strobj' , ctypes.py_object ),
    ]


wrapperbase_p = ctypes.POINTER(wrapperbase)


### Various kinds of descriptor objects


from .object import PyObject_HEAD, PyTypeObject_p
from .methodobject import PyMethodDef_p
from .structmember import PyMemberDef_p
from .cpython.object import vectorcallfunc


class PyDescrObject(ctypes.Structure):
    """
    PyObject_HEAD
    PyTypeObject *d_type;
    PyObject *d_name;
    PyObject *d_qualname;
    """

    _anonymous_ = ('ob_base',)
    _fields_ = [
        *PyObject_HEAD,
        ('d_type'     , PyTypeObject_p   ),
        ('d_name'     , ctypes.py_object ),
        ('d_qualname' , ctypes.py_object ),
    ]


PyDescrObject_p = ctypes.POINTER(PyDescrObject)
PyDescr_COMMON = (
    ('d_common' , PyDescrObject ),
)


###


class PyMethodDescrObject(ctypes.Structure):
    """
    PyDescr_COMMON;
    PyMethodDef *d_method;
    vectorcallfunc vectorcall;
    """

    _anonymous_ = ('d_common',)
    _fields_ = [
        *PyDescr_COMMON,
        ('d_method'   , PyMethodDef_p  ),
        ('vectorcall' , vectorcallfunc ),
    ]


PyMethodDescrObject_p = ctypes.POINTER(PyMethodDescrObject)


###


class PyMemberDescrObject(ctypes.Structure):
    """
    PyDescr_COMMON;
    struct PyMemberDef *d_member;
    """

    _anonymous_ = ('d_common',)
    _fields_ = [
        *PyDescr_COMMON,
        ('d_member' , PyMemberDef_p ),
    ]


PyMemberDescrObject_p = ctypes.POINTER(PyMemberDescrObject)


###


class PyGetSetDescrObject(ctypes.Structure):
    """
    PyDescr_COMMON;
    PyGetSetDef *d_getset;
    """

    _anonymous_ = ('d_common',)
    _fields_ = [
        *PyDescr_COMMON,
        ('d_getset' , PyGetSetDef_p ),
    ]


PyGetSetDescrObject_p = ctypes.POINTER(PyGetSetDescrObject)


###


class PyWrapperDescrObject(ctypes.Structure):
    """
    PyDescr_COMMON;
    struct wrapperbase *d_base;
    void *d_wrapped;
    """

    _anonymous_ = ('d_common',)
    _fields_ = [
        *PyDescr_COMMON,
        ('d_base'    , wrapperbase     ),
        # This can be any function pointer
        ('d_wrapped' , ctypes.c_void_p ),
    ]


PyWrapperDescrObject_p = ctypes.POINTER(PyWrapperDescrObject)
