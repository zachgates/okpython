__all__ = [
    'PyBytesObject', 'PyBytesObject_p',
    'PyBytes_AS_STRING', 'PyBytes_GET_SIZE',
    '_PyBytesWriter', '_PyBytesWriter_p',

]


import ctypes

from ... import PyAPI_FUNC


###


from ..object import PyVarObject


class PyBytesObject(ctypes.Structure):
    """
    PyObject_VAR_HEAD
    Py_hash_t ob_shash;
    char ob_sval[1];
    """

    # Invariants:
    #   - ob_sval contains space for 'ob_size+1' elements.
    #   - ob_sval[ob_size] == 0.
    #   - ob_shash is the hash of the string or -1 if not computed yet.

    # Caching the hash (ob_shash) saves recalculation of a string's
    # hash value. This significantly speeds up dict lookups.

    _anonymous_ = ('ob_base',)
    _fields_ = [
        ('ob_base'  , PyVarObject                   ),
        ('ob_shash' , ctypes.py_hash_t              ),
        ('_ob_sval' , ctypes.POINTER(ctypes.c_char) ),
    ]

    @property
    def ob_sval(self):
        address = ctypes.addressof(self._ob_sval)
        arr_t = ctypes.ARRAY(self._ob_sval._type_, self.ob_size + 1)
        return arr_t.from_address(address)


PyBytesObject_p = ctypes.POINTER(PyBytesObject)


"""
import random, string
b = ''.join(random.choices(string.hexdigits, k=10)).encode()
ob = PyBytesObject.from_address(id(b))

assert (ob.ob_shash == -1)
assert (hash(b) == ob.ob_shash)
assert (ob.ob_sval[ob.ob_size] == 0)
"""


###


from ..object import PyObject_p, PyObject_pp


PyAPI_FUNC("_PyBytes_Resize",
    restype = ctypes.c_int,
    argtypes = [
        PyObject_pp,
        ctypes.py_ssize_t,
    ])

PyAPI_FUNC("_PyBytes_FormatEx",
    restype = PyObject_p,
    argtypes = [
        ctypes.c_char_p,   # format
        ctypes.py_ssize_t, # format_len
        PyObject_p,        # args
        ctypes.c_int,      # use_bytearray
    ])

PyAPI_FUNC("_PyBytes_FromHex",
    restype = PyObject_p,
    argtypes = [
        PyObject_p,   # string
        ctypes.c_int, # use_bytearray
    ])

# Helper for PyBytes_DecodeEscape that detects invalid escape chars.
PyAPI_FUNC("_PyBytes_DecodeEscape",
    restype = PyObject_p,
    argtypes = [
        ctypes.c_char_p,
        ctypes.py_ssize_t,
        ctypes.c_char_p,
        ctypes.c_char_pp,
    ])

# _PyBytes_Join(sep, x) is like sep.join(x).  sep must be PyBytesObject*,
# x must be an iterable object.
PyAPI_FUNC("_PyBytes_Join",
    restype = PyObject_p,
    argtypes = [
        PyObject_p, # sep
        PyObject_p, # x
    ])


###


from ..object import Py_SIZE
from ..bytesobject import PyBytes_Check


def PyBytes_AS_STRING(op):
    """
    #define PyBytes_AS_STRING(op) (assert(PyBytes_Check(op)), \
                                    (((PyBytesObject *)(op))->ob_sval))
    """
    assert PyBytes_Check(op)
    op = ctypes.cast(ctypes.byref(op), PyBytesObject_p)
    return op.contents.ob_sval.raw[:-1]


def PyBytes_GET_SIZE(op):
    """
    #define PyBytes_GET_SIZE(op)  (assert(PyBytes_Check(op)),Py_SIZE(op))
    """
    assert PyBytes_Check(op)
    return Py_SIZE(op)


###


class _PyBytesWriter(ctypes.Structure):
    """
    PyObject *buffer;
    Py_ssize_t allocated;
    Py_ssize_t min_size;
    int use_bytearray;
    int overallocate;
    int use_small_buffer;
    char small_buffer[512];
    """

    # The _PyBytesWriter structure is big:
    # it contains an embedded "stack buffer".
    #
    # A _PyBytesWriter variable must be declared at the end of variables in a
    # function to optimize the memory allocation on the stack.

    _fields_ = [
        # bytes, bytearray or NULL (when the small buffer is used)
        ('buffer'           , ctypes.py_object                 ),

        # Number of allocated size.
        ('allocated'        , ctypes.py_ssize_t                ),

        # Minimum number of allocated bytes,
        # incremented by _PyBytesWriter_Prepare()
        ('min_size'         , ctypes.py_ssize_t                ),

        # If non-zero, use a bytearray instead of a bytes object for buffer.
        ('use_bytearray'    , ctypes.c_int                     ),

        # If non-zero, overallocate the buffer (default: 0).
        # This flag must be zero if use_bytearray is non-zero.
        ('overallocate'     , ctypes.c_int                     ),

        # Stack buffer
        ('use_small_buffer' , ctypes.c_int                     ),
        ('small_buffer'     , ctypes.ARRAY(ctypes.c_char, 512) ),
    ]


_PyBytesWriter_p = ctypes.POINTER(_PyBytesWriter)


###


# Initialize a bytes writer
# By default, the overallocation is disabled.
# Set the overallocate attribute to control the allocation of the buffer.
PyAPI_FUNC("_PyBytesWriter_Init",
    argtypes = [
        _PyBytesWriter_p, # writer
    ])

# Get the buffer content and reset the writer.
# - Return a bytes object, or a bytearray object if use_bytearray is non-zero.
# - Raise an exception and return NULL on error.
PyAPI_FUNC("_PyBytesWriter_Finish",
    restype = PyObject_p,
    argtypes = [
        _PyBytesWriter_p, # writer
        ctypes.c_void_p,  # str
    ])

# Deallocate memory of a writer (clear its internal buffer).
PyAPI_FUNC("_PyBytesWriter_Dealloc",
    argtypes = [
        _PyBytesWriter_p, # writer
    ])

# Allocate the buffer to write size bytes.
# - Return the pointer to the beginning of buffer data.
# - Raise an exception and return NULL on error.
PyAPI_FUNC("_PyBytesWriter_Alloc",
    restype = ctypes.c_void_p,
    argtypes = [
        _PyBytesWriter_p,  # writer
        ctypes.py_ssize_t, # size
    ])

# Ensure that the buffer is large enough to write *size* bytes.
# Add size to the writer minimum size (min_size attribute).
# - str is the current pointer inside the buffer.
# - Return the updated current pointer inside the buffer.
# - Raise an exception and return NULL on error.
PyAPI_FUNC("_PyBytesWriter_Prepare",
    restype = ctypes.c_void_p,
    argtypes = [
        _PyBytesWriter_p,  # writer
        ctypes.c_void_p,   # str
        ctypes.py_ssize_t, # size
    ])

# Resize the buffer to make it larger.
# The new buffer may be larger than size bytes because of overallocation.
# - Return the updated current pointer inside the buffer.
# - Raise an exception and return NULL on error.
# Note: size must be greater than the number of allocated bytes in the writer.
# This function doesn't use the writer minimum size (min_size attribute).
# See also _PyBytesWriter_Prepare().
PyAPI_FUNC("_PyBytesWriter_Resize",
    restype = ctypes.c_void_p,
    argtypes = [
        _PyBytesWriter_p,  # writer
        ctypes.c_void_p,   # str
        ctypes.py_ssize_t, # size
    ])

# Write bytes.
# - Raise an exception and return NULL on error.
PyAPI_FUNC("_PyBytesWriter_WriteBytes",
    restype = ctypes.c_void_p,
    argtypes = [
        _PyBytesWriter_p,  # writer
        ctypes.c_void_p,   # str
        ctypes.c_void_p,   # bytes
        ctypes.py_ssize_t, # size
    ])
