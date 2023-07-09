__all__ = [
    'PyFunctionObject', 'PyFunctionObject_p',
]


import ctypes


###


from .object import PyObject_HEAD
from .cpython.object import vectorcallfunc


class PyFunctionObject(ctypes.Structure):
    """
    PyObject_HEAD
    PyObject *func_code;
    PyObject *func_globals;
    PyObject *func_defaults;
    PyObject *func_kwdefaults;
    PyObject *func_closure;
    PyObject *func_doc;
    PyObject *func_name;
    PyObject *func_dict;
    PyObject *func_weakreflist;
    PyObject *func_module;
    PyObject *func_annotations;
    PyObject *func_qualname;
    vectorcallfunc vectorcall;
    """

    # Invariant:
    #   func_closure contains the bindings for func_code->co_freevars, so
    #   PyTuple_Size(func_closure) == PyCode_GetNumFree(func_code)
    #   (func_closure may be NULL if PyCode_GetNumFree(func_code) == 0).

    _fields_ = [
        *PyObject_HEAD,
        # A code object, the __code__ attribute
        ('func_code'        , ctypes.py_object ),
        # A dictionary (other mappings won't do)
        ('func_globals'     , ctypes.py_object ),
        # NULL or a tuple
        ('func_defaults'    , ctypes.py_object ),
        # NULL or a dict
        ('func_kwdefaults'  , ctypes.py_object ),
        # NULL or a tuple of cell objects
        ('func_closure'     , ctypes.py_object ),
        # The __doc__ attribute, can be anything
        ('func_doc'         , ctypes.py_object ),
        # The __name__ attribute, a string object
        ('func_name'        , ctypes.py_object ),
        # The __dict__ attribute, a dict or NULL
        ('func_dict'        , ctypes.py_object ),
        # List of weak references
        ('func_weakreflist' , ctypes.py_object ),
        # The __module__ attribute, can be anything
        ('func_module'      , ctypes.py_object ),
        # Annotations, a dict or NULL
        ('func_annotations' , ctypes.py_object ),
        # The qualified name
        ('func_qualname'    , ctypes.py_object ),
        ('vectorcall'       , vectorcallfunc   ),
    ]


PyFunctionObject_p = ctypes.POINTER(PyFunctionObject)
