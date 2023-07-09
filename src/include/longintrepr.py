__all__ = [
    'digit', 'sdigit', 'twodigits', 'stwodigits',
    '_PyLong_DECIMAL_SHIFT', '_PyLong_DECIMAL_BASE',
    'PyLong_SHIFT', 'PyLong_BASE', 'PyLong_MASK',
    'PyLongObject', 'PyLongObject_p',
]


import ctypes


###


from .pyport import PYLONG_BITS_IN_DIGIT


# Type 'digit' should be able to hold 2*PyLong_BASE-1, and type 'twodigits'
# should be an unsigned integer type able to hold all integers up to
# PyLong_BASE*PyLong_BASE-1.


if PYLONG_BITS_IN_DIGIT == 30:
    digit = ctypes.c_uint32
    sdigit = ctypes.c_int32 # signed variant of digit

    twodigits = ctypes.c_uint64
    stwodigits = ctypes.c_int64 # signed variant of twodigits

    _PyLong_DECIMAL_SHIFT = 9 # max(e such that 10**e fits in a digit)
    _PyLong_DECIMAL_BASE = digit(1_000_000_000) # 10 ** DECIMAL_SHIFT

elif PYLONG_BITS_IN_DIGIT == 15:
    digit = ctypes.c_ushort
    sdigit = ctypes.c_short # signed variant of digit

    twodigits = ctypes.c_ulong
    stwodigits = ctypes.c_long # signed variant of twodigits

    _PyLong_DECIMAL_SHIFT = 4 # max(e such that 10**e fits in a digit)
    _PyLong_DECIMAL_BASE = digit(10_000) # 10 ** DECIMAL_SHIFT

else:
    raise ValueError('PYLONG_BITS_IN_DIGIT should be 15 or 30')


PyLong_SHIFT = PYLONG_BITS_IN_DIGIT
PyLong_BASE = digit(1 << PyLong_SHIFT)
PyLong_MASK = digit(PyLong_BASE.value - 1)


###


import sys

from .object import PyObject_VAR_HEAD


class PyLongObject(ctypes.Structure):
    """
    PyObject_VAR_HEAD
    digit ob_digit[1];
    """

    _anonymous_ = ('ob_base',)
    _fields_ = [
        *PyObject_VAR_HEAD,
        ('_ob_digit' , ctypes.POINTER(digit) ),
    ]

    @property
    def ob_digit(self):
        address = ctypes.addressof(self._ob_digit)
        arr_t = ctypes.ARRAY(self._ob_digit._type_, abs(self.ob_size))
        return arr_t.from_address(address)


PyLongObject_p = ctypes.POINTER(PyLongObject)


"""
n = int(
    'C694C69D8F5650C1A58DA8EBBE049B73D88C1BD2'
    '46B18DA8835A53157D54D2859940796ACCCE6332'
    'A1A', base = 16)
ob = PyLongObject.from_address(id(n))

k = 0
for index, section in enumerate(ob.ob_digit):
    section *= (1 << (PyLong_SHIFT * index))
    k += section

assert k == n
"""
