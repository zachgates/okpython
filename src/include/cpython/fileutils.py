__all__ = [
    '_Py_stat_struct', '_Py_stat_struct_p',
]


import ctypes

from ... import PyAPI_FUNC
from ..object import PyObject_p


###


# typedef enum {
#     _Py_ERROR_UNKNOWN=0,
#     _Py_ERROR_STRICT,
#     _Py_ERROR_SURROGATEESCAPE,
#     _Py_ERROR_REPLACE,
#     _Py_ERROR_IGNORE,
#     _Py_ERROR_BACKSLASHREPLACE,
#     _Py_ERROR_SURROGATEPASS,
#     _Py_ERROR_XMLCHARREFREPLACE,
#     _Py_ERROR_OTHER
# } _Py_error_handler;


PyAPI_FUNC("_Py_GetErrorHandler",
    restype = ctypes.c_int, # _Py_error_handler
    argtypes = [
        ctypes.c_char_p, # errors
    ])

PyAPI_FUNC("_Py_DecodeLocaleEx",
    restype = ctypes.c_int,
    argtypes = [
        ctypes.c_char_p,   # arg
        ctypes.c_wchar_pp, # wstr
        ctypes.c_size_t_p, # wlen
        ctypes.c_char_pp,  # reason
        ctypes.c_int,      # current_locale
        ctypes.c_int,      # _Py_error_handler errors
    ])

PyAPI_FUNC("_Py_EncodeLocaleEx",
    restype = ctypes.c_int,
    argtypes = [
        ctypes.c_wchar_p,  # text
        ctypes.c_char_pp,  # str
        ctypes.c_size_t_p, # error_pos
        ctypes.c_char_pp,  # reason
        ctypes.c_int,      # current_locale
        ctypes.c_int,      # _Py_error_handler errors
    ])

PyAPI_FUNC("_Py_device_encoding",
    restype = PyObject_p,
    argtypes = [
        ctypes.c_int,
    ])


###


if ctypes.pyconfig.MS_WINDOWS:
    class _Py_stat_struct(ctypes.Structure):
        """
        unsigned long st_dev;
        uint64_t st_ino;
        unsigned short st_mode;
        int st_nlink;
        int st_uid;
        int st_gid;
        unsigned long st_rdev;
        __int64 st_size;
        time_t st_atime;
        int st_atime_nsec;
        time_t st_mtime;
        int st_mtime_nsec;
        time_t st_ctime;
        int st_ctime_nsec;
        unsigned long st_file_attributes;
        unsigned long st_reparse_tag;
        """

        _fields_ = [
            ('st_dev'             , ctypes.c_ulong  ),
            ('st_ino'             , ctypes.c_uint64 ),
            ('st_mode'            , ctypes.c_ushort ),
            ('st_nlink'           , ctypes.c_int    ),
            ('st_uid'             , ctypes.c_int    ),
            ('st_gid'             , ctypes.c_int    ),
            ('st_rdev'            , ctypes.c_ulong  ),
            ('st_size'            , ctypes.c_int64  ),
            ('st_atime'           , ctypes.c_ulong  ),
            ('st_atime_nsec'      , ctypes.c_int    ),
            ('st_mtime'           , ctypes.c_ulong  ),
            ('st_mtime_nsec'      , ctypes.c_int    ),
            ('st_ctime'           , ctypes.c_ulong  ),
            ('st_ctime_nsec'      , ctypes.c_int    ),
            ('st_file_attributes' , ctypes.c_ulong  ),
            ('st_reparse_tag'     , ctypes.c_ulong  ),
        ]
else:
    _Py_stat_struct = ctypes.c_void_p


_Py_stat_struct_p = ctypes.POINTER(_Py_stat_struct)


###


PyAPI_FUNC("_Py_fstat",
    restype = ctypes.c_int,
    argtypes = [
        ctypes.c_int,      # fd
        _Py_stat_struct_p, # status
    ])

PyAPI_FUNC("_Py_fstat_noraise",
    restype = ctypes.c_int,
    argtypes = [
        ctypes.c_int,      # fd
        _Py_stat_struct_p, # status
    ])

PyAPI_FUNC("_Py_stat",
    restype = ctypes.c_int,
    argtypes = [
        PyObject_p,      # path
        ctypes.c_void_p, # struct stat *status
    ])

PyAPI_FUNC("_Py_open",
    restype = ctypes.c_int,
    argtypes = [
        ctypes.c_char_p, # pathname
        ctypes.c_int,    # flags
    ])

PyAPI_FUNC("_Py_open_noraise",
    restype = ctypes.c_int,
    argtypes = [
        ctypes.c_char_p, # pathname
        ctypes.c_int,    # flags
    ])

PyAPI_FUNC("_Py_wfopen",
    restype = ctypes.c_void_p, # FILE *
    argtypes = [
        ctypes.c_wchar_p, # path
        ctypes.c_wchar_p, # mode
    ])

# PyAPI_FUNC("_Py_fopen",
#     restype = ctypes.c_void_p, # FILE *
#     argtypes = [
#         ctypes.c_char_p, # pathname
#         ctypes.c_char_p, # mode
#     ])

PyAPI_FUNC("_Py_fopen_obj",
    restype = ctypes.c_void_p, # FILE *
    argtypes = [
        PyObject_p,      # path
        ctypes.c_char_p, # mode
    ])

PyAPI_FUNC("_Py_read",
    restype = ctypes.py_ssize_t,
    argtypes = [
        ctypes.c_int,    # fd
        ctypes.c_void_p, # buf
        ctypes.c_size_t, # count
    ])

PyAPI_FUNC("_Py_write",
    restype = ctypes.py_ssize_t,
    argtypes = [
        ctypes.c_int,    # fd
        ctypes.c_void_p, # buf
        ctypes.c_size_t, # count
    ])

PyAPI_FUNC("_Py_write_noraise",
    restype = ctypes.py_ssize_t,
    argtypes = [
        ctypes.c_int,    # fd
        ctypes.c_void_p, # buf
        ctypes.c_size_t, # count
    ])


if ctypes.pyconfig.HAVE_READLINK:
    PyAPI_FUNC("_Py_wreadlink",
        restype = ctypes.c_int,
        argtypes = [
            ctypes.c_wchar_p, # path
            ctypes.c_wchar_p, # buf
            # Number of characters of 'buf' buffer
            # including the trailing NUL character
            ctypes.c_size_t,  # buflen
        ])
else:
    _Py_wreadlink = None


if ctypes.pyconfig.HAVE_REALPATH:
    PyAPI_FUNC("_Py_wrealpath",
        restype = ctypes.c_wchar_p,
        argtypes = [
            ctypes.c_wchar_p, # path
            ctypes.c_wchar_p, # resolved_path
            # Number of characters of 'resolved_path' buffer
            # including the trailing NUL character
            ctypes.c_size_t,  # resolved_path_len
        ])
else:
    _Py_wrealpath = None


if not ctypes.pyconfig.MS_WINDOWS:
    PyAPI_FUNC("_Py_isabs",
        restype = ctypes.c_int,
        argtypes = [
            ctypes.c_wchar_p, # path
        ])
else:
    _Py_isabs = None


PyAPI_FUNC("_Py_abspath",
    restype = ctypes.c_int,
    argtypes = [
        ctypes.c_wchar_p,  # path
        ctypes.c_wchar_pp, # abspath_p
    ])

PyAPI_FUNC("_Py_wgetcwd",
    restype = ctypes.c_wchar_p,
    argtypes = [
        ctypes.c_wchar_p, # buf
        # Number of characters of 'buf' buffer
        # including the trailing NUL character
        ctypes.c_size_t,  # buflen
    ])

PyAPI_FUNC("_Py_get_inheritable",
    restype = ctypes.c_int,
    argtypes = [
        ctypes.c_int, # fd
    ])

PyAPI_FUNC("_Py_set_inheritable",
    restype = ctypes.c_int,
    argtypes = [
        ctypes.c_int,   # fd
        ctypes.c_int,   # inheritable
        ctypes.c_int_p, # atomic_flag_works
    ])

PyAPI_FUNC("_Py_set_inheritable_async_safe",
    restype = ctypes.c_int,
    argtypes = [
        ctypes.c_int,   # fd
        ctypes.c_int,   # inheritable
        ctypes.c_int_p, # atomic_flag_works
    ])

PyAPI_FUNC("_Py_dup",
    restype = ctypes.c_int,
    argtypes = [
        ctypes.c_int, # fd
    ])


if not ctypes.pyconfig.MS_WINDOWS:
    PyAPI_FUNC("_Py_get_blocking",
        restype = ctypes.c_int,
        argtypes = [
            ctypes.c_int, # fd
        ])

    PyAPI_FUNC("_Py_set_blocking",
        restype = ctypes.c_int,
        argtypes = [
            ctypes.c_int, # fd
            ctypes.c_int, # blocking
        ])
else:
    _Py_get_blocking = None
    _Py_set_blocking = None
