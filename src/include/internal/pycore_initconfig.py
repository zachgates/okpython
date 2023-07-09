__all__ = [
    '_PyArgv', '_PyArgv_p',
    '_PyPreCmdline', '_PyPreCmdline_p',
]


import ctypes


###


class _PyArgv(ctypes.Structure):
    """
    Py_ssize_t argc;
    int use_bytes_argv;
    char * const *bytes_argv;
    wchar_t * const *wchar_argv;
    """

    _fields_ = [
        ('argc'           , ctypes.py_ssize_t ),
        ('use_bytes_argv' , ctypes.c_int      ),
        ('bytes_argv'     , ctypes.c_char_pp  ),
        ('wchar_argv'     , ctypes.c_wchar_pp ),
    ]


_PyArgv_p = ctypes.POINTER(_PyArgv)


###


from ..cpython.initconfig import PyWideStringList


class _PyPreCmdline(ctypes.Structure):
    """
    PyWideStringList argv;
    PyWideStringList xoptions;
    int isolated;
    int use_environment;
    int dev_mode;
    """

    _fields_ = [
        ('argv'            , PyWideStringList ),
        ('xoptions'        , PyWideStringList ), # "-X value" option
        ('isolated'        , ctypes.c_int     ), # -I option
        ('use_environment' , ctypes.c_int     ), # -E option
        ('dev_mode'        , ctypes.c_int     ), # -X dev and PYTHONDEVMODE
    ]


_PyPreCmdline_p = ctypes.POINTER(_PyPreCmdline)
