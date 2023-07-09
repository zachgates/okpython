__all__ = [
    'PyMethodDef', 'PyMethodDef_p',
    'MLFLAGS', 'METH',
]


import ctypes


###


class PyMethodDef(ctypes.Structure):
    """
    const char *ml_name;
    PyCFunction ml_meth;
    int ml_flags;
    const char *ml_doc;
    """

    _fields_ = [
        # The name of the built-in function/method
        ('ml_name'  , ctypes.c_char_p  ),

        # The C function that implements it
        ('ml_meth'  , ctypes.py_object ), # XXX: this is wrong

        # Combination of METH_xxx flags, which mostly describe the args
        # expected by the C func
        ('ml_flags' , ctypes.c_int     ),

        # The __doc__ attribute, or NULL
        ('ml_doc'   , ctypes.c_char_p  ),
    ]


PyMethodDef_p = ctypes.POINTER(PyMethodDef)


###


from .. import FlagGroup


class MLFLAGS(FlagGroup):
    """
    Flag passed to newmethodobject
    """

    def __str__(self):
        return f'METH_{self._name_}'

    OLDARGS   = ( 0 << 0 ) # unsupported now
    VARARGS   = ( 1 << 0 )
    KEYWORDS  = ( 1 << 1 )

    # METH_NOARGS and METH_O must not be combined with the flags above.
    NOARGS    = ( 1 << 2 )
    O         = ( 1 << 3 )

    # METH_CLASS and METH_STATIC are a little different; these control
    # the construction of methods for a class. These cannot be used for
    # functions in modules.
    CLASS     = ( 1 << 4 )
    STATIC    = ( 1 << 5 )

    # METH_COEXIST allows a method to be entered even though a slot has
    # already filled the entry.  When defined, the flag allows a separate
    # method, "__contains__" for example, to coexist with a defined
    # slot like sq_contains.
    COEXIST   = ( 1 << 6 )

    FASTCALL  = ( 1 << 7 )

    # This bit is preserved for Stackless Python
    STACKLESS = ( 1 << 8 )

    # METH_METHOD means the function stores an additional reference to the
    # class that defines it; both self and class are passed to it.
    # It uses PyCMethodObject instead of PyCFunctionObject.
    # May not be combined with METH_NOARGS, METH_O, METH_CLASS or METH_STATIC.
    METHOD    = ( 1 << 9 )


METH = MLFLAGS._select
