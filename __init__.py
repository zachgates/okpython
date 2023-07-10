import _ctypes
import ctypes
import ctypes.util
import os
import platform
import struct
import sys
import sysconfig
import types

from pprint import pprint


###


ctypes.pyconfig = types.SimpleNamespace()


def _update_pyconfig(dct):
    for key, val in dct.items():
        setattr(ctypes.pyconfig, key, val)


with open(sysconfig.get_config_h_filename(), 'r') as f:
    _update_pyconfig(sysconfig.parse_config_h(f))


_update_pyconfig({ # processor
    '__i386__': (platform.machine() == 'i386'),
    '__x86_64__': (platform.machine() == 'x86_64'),
    '__ppc__': (platform.machine() == 'ppc'),
    '__ppc64__': (platform.machine() == 'ppc64'),
    })


_update_pyconfig({ # architecture
    '__LP64__': (8 * struct.calcsize('P') == 64),
    '__BIG_ENDIAN__': (sys.byteorder == 'big'),
    '__LITTLE_ENDIAN__': (sys.byteorder == 'little'),
    })


_update_pyconfig({ # platform
    'MS_WINDOWS': sys.platform.startswith('win32'),
    '__APPLE__': sys.platform.startswith('darwin'),
    '__CYGWIN__': sys.platform.startswith('cygwin'),
    '__VXWORKS__': sys.platform.startswith('vxworks'),
    '_AIX': sys.platform.startswith('aix'),
    })


_update_pyconfig({ # features
    'HAVE_DLOPEN': hasattr(sys, 'getdlopenflags'),
    'HAVE_FORK': hasattr(os, 'fork'),
    })


###


if not hasattr(ctypes.pyconfig, 'Py_DEBUG'):
    ctypes.pyconfig.Py_DEBUG = sys.flags.debug


# Py_DEBUG implies Py_REF_DEBUG.
ctypes.pyconfig.Py_REF_DEBUG = ctypes.pyconfig.Py_DEBUG


if not hasattr(ctypes.pyconfig, 'Py_TRACE_REFS'):
    ctypes.pyconfig.Py_TRACE_REFS = hasattr(sys, 'getobjects')


# Py_LIMITED_API is incompatible with Py_DEBUG, Py_TRACE_REFS, and Py_REF_DEBUG
ctypes.pyconfig.Py_LIMITED_API = (
    not (ctypes.pyconfig.Py_DEBUG
         or ctypes.pyconfig.Py_TRACE_REFS
         )
    )


###


if (hasattr(ctypes.pyconfig, 'MS_WIN32')
    or hasattr(ctypes.pyconfig, 'MS_WIN64')):
    ctypes.pyconfig.MS_WINDOWS = True


if ctypes.pyconfig.MS_WINDOWS:
    ctypes.pyconfig.__GNUC__ = (ctypes.pyconfig.COMPILER == '"[gcc]"')
    ctypes.pyconfig.__LCC__ = (ctypes.pyconfig.COMPILER == '"[lcc-win32]"')


if ctypes.pyconfig.__APPLE__:
    ctypes.pyconfig.__clang__ = ('Clang' in platform.python_compiler())
    ctypes.pyconfig.__GNUC__ = ('GCC' in platform.python_compiler())


###


if ctypes.pyconfig.MS_WINDOWS:
    ctypes.capi = ctypes.windll.msvcrt
else:
    ctypes.capi = ctypes.PyDLL(ctypes.util.find_library('libc'))


###

ctypes.c_size_t_p = ctypes.POINTER(ctypes.c_size_t)


if sys.version_info > (2, 4):
    ctypes.py_ssize_t = ctypes.c_size_t
else:
    ctypes.py_ssize_t = ctypes.c_int


ctypes.py_ssize_t_p = ctypes.POINTER(ctypes.py_ssize_t)


if ctypes.pyconfig.__LP64__:
    ctypes.py_hash_t = ctypes.c_int64
else:
    ctypes.py_hash_t = ctypes.c_int32


ctypes.py_hash_t_p = ctypes.POINTER(ctypes.py_hash_t)


ctypes.c_void_pp = ctypes.POINTER(ctypes.c_void_p)


ctypes.c_int_p = ctypes.POINTER(ctypes.c_int)


ctypes.c_uint_p = ctypes.POINTER(ctypes.c_uint)


ctypes.c_char_pp = ctypes.POINTER(ctypes.c_char_p)
ctypes.c_char_ppp = ctypes.POINTER(ctypes.c_char_pp)


ctypes.c_wchar_pp = ctypes.POINTER(ctypes.c_wchar_p)
ctypes.c_wchar_ppp = ctypes.POINTER(ctypes.c_wchar_pp)


ctypes.py_object_p = ctypes.POINTER(ctypes.py_object)


ctypes.va_list = ctypes.c_char_p


###


ctypes.IS_POINTER = lambda v: isinstance(v, _ctypes._Pointer)
ctypes.IS_NULLPTR = lambda v: (ctypes.IS_POINTER(v) and not bool(v))
