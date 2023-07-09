__all__ = [
    'PYLONG_BITS_IN_DIGIT', 'PY_FORMAT_SIZE_T',
    'SIZEOF_LONG', 'LONG_MAX', 'LONG_MIN', 'LONG_BIT',
    'PY_BIG_ENDIAN', 'PY_LITTLE_ENDIAN',
    'PY_DWORD_MAX',
]


import ctypes


### sys.int_info.bits_per_digit


if ctypes.pyconfig.__LP64__:
    PYLONG_BITS_IN_DIGIT = 30
else:
    PYLONG_BITS_IN_DIGIT = 15


###


PY_FORMAT_SIZE_T  = "z"


###


SIZEOF_LONG = ctypes.sizeof(ctypes.c_long)

if SIZEOF_LONG == 4:
    LONG_MAX = pow(2, 31) - 1 # 0X7FFFFFFFL
elif SIZEOF_LONG == 8:
    LONG_MAX = pow(2, 63) - 1 # 0X7FFFFFFFFFFFFFFFL
else:
    raise RuntimeError('could not set LONG_MAX in pyport')

LONG_MIN = (-LONG_MAX - 1)
LONG_BIT = (8 * SIZEOF_LONG)


###


if ctypes.pyconfig.__BIG_ENDIAN__:
    PY_BIG_ENDIAN = True
    PY_LITTLE_ENDIAN = False
else:
    PY_BIG_ENDIAN = False
    PY_LITTLE_ENDIAN = True


###


# Maximum value of the Windows DWORD type
PY_DWORD_MAX = pow(2, 32) - 1 # 4294967295
