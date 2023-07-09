__all__ = [
    '_PyArg_Parser', '_PyArg_Parser_p',
]


import ctypes


###


class _PyArg_Parser(ctypes.Structure):
    """
    const char *format;
    const char * const *keywords;
    const char *fname;
    const char *custom_msg;
    int pos;
    int min;
    int max;
    PyObject *kwtuple;
    struct _PyArg_Parser *next;
    """


_PyArg_Parser_p = ctypes.POINTER(_PyArg_Parser)
_PyArg_Parser._fields_ = [
    ('format'     , ctypes.c_char_p  ),
    ('keywords'   , ctypes.c_char_pp ),
    ('fname'      , ctypes.c_char_p  ),
    ('custom_msg' , ctypes.c_char_p  ),
    # number of positional-only arguments
    ('pos'        , ctypes.c_int     ),
    # minimal number of arguments
    ('min'        , ctypes.c_int     ),
    # maximal number of positional arguments
    ('max'        , ctypes.c_int     ),
    # tuple of keyword parameter names
    ('kwtuple'    , ctypes.py_object ),
    ('next'       , _PyArg_Parser_p  ),
]
