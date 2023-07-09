__all__ = [
    '_Py_CODEUNIT', '_Py_OPCODE', '_Py_OPARG',
    'PyCodeObject', 'PyCodeObject_p',
    'COFLAGS',
    'PyCode_Check', 'PyCode_GetNumFree',
    'PyAddrPair', 'PyAddrPair_p',
]


import ctypes

from ... import PyAPI_DATA, PyAPI_FUNC
from ..object import PyObject_p


###


_Py_CODEUNIT = ctypes.c_uint16


if ctypes.pyconfig.__BIG_ENDIAN__:
    _Py_OPCODE = lambda word: (word >> 8)
    _Py_OPARG = lambda word: (word & 255)
else:
    _Py_OPCODE = lambda word: (word & 255)
    _Py_OPARG = lambda word: (word >> 8)


###


from ..object import PyObject_HEAD
from ..internal.pycore_code import _PyOpcache_p


class PyCodeObject(ctypes.Structure):
    """
    PyObject_HEAD
    int co_argcount;
    int co_posonlyargcount;
    int co_kwonlyargcount;
    int co_nlocals;
    int co_stacksize;
    int co_flags;
    int co_firstlineno;
    PyObject *co_code;
    PyObject *co_consts;
    PyObject *co_names;
    PyObject *co_varnames;
    PyObject *co_freevars;
    PyObject *co_cellvars;
    Py_ssize_t *co_cell2arg;
    PyObject *co_filename;
    PyObject *co_name;
    PyObject *co_lnotab;
    void *co_zombieframe;
    PyObject *co_weakreflist;
    void *co_extra;
    unsigned char *co_opcache_map;
    _PyOpcache *co_opcache;
    int co_opcache_flag;
    unsigned char co_opcache_size;
    """

    # Bytecode object

    _anonymous_ = ('ob_base',)
    _fields_ = [
        *PyObject_HEAD,
        # #arguments, except *args
        ('co_argcount'        , ctypes.c_int      ),
        # #positional only arguments
        ('co_posonlyargcount' , ctypes.c_int      ),
        # #keyword only arguments
        ('co_kwonlyargcount'  , ctypes.c_int      ),
        # #local variables
        ('co_nlocals'         , ctypes.c_int      ),
        # #entries needed for evaluation stack
        ('co_stacksize'       , ctypes.c_int      ),
        # CO_..., see below
        ('co_flags'           , ctypes.c_int      ),
        # first source line number
        ('co_firstlineno'     , ctypes.c_int      ),
        # instruction opcodes
        ('co_code'            , PyObject_p        ),
        # list (constants used)
        ('co_consts'          , PyObject_p        ),
        # list of strings (names used)
        ('co_names'           , PyObject_p        ),
        # tuple of strings (local variable names)
        ('co_varnames'        , PyObject_p        ),
        # tuple of strings (free variable names)
        ('co_freevars'        , PyObject_p        ),
        # tuple of strings (cell variable names)
        ('co_cellvars'        , PyObject_p        ),

        # The rest aren't used in either hash or comparisons, except for
        # co_name, used in both. This is done to preserve the name and line
        # number for tracebacks and debuggers; otherwise, constant
        # de-duplication would collapse identical functions/lambdas defined
        # on different lines.

        # Maps cell vars which are arguments.
        ('co_cell2arg'        , ctypes.py_ssize_t ),
        # unicode (where it was loaded from)
        ('co_filename'        , PyObject_p        ),
        # unicode (name, for reference)
        ('co_name'            , PyObject_p        ),
        # string (encoding addr<->lineno mapping)
        ('co_lnotab'          , PyObject_p        ),
        # for optimization only (see frameobject.c)
        ('co_zombieframe'     , ctypes.c_void_p   ),
        # to support weakrefs to code objects
        ('co_weakreflist'     , PyObject_p        ),
        # Scratch space for extra data relating to the code object.
        ('co_extra'           , ctypes.c_void_p   ),

        # Per opcodes just-in-time cache
        # To reduce cache size, we use indirect mapping from opcode index to
        # cache object:
        #   - cache = co_opcache[co_opcache_map[next_instr - first_instr] - 1]

        # co_opcache_map is indexed by (next_instr - first_instr).
        #   - 0 means there is no cache for this opcode.
        #   - n > 0 means there is cache in co_opcache[n-1].
        ('co_opcache_map'     , ctypes.c_ubyte    ),
        ('co_opcache'         , _PyOpcache_p      ),
        # used to determine when create a cache.
        ('co_opcache_flag'    , ctypes.c_int      ),
        # length of co_opcache.
        ('co_opcache_size'    , ctypes.c_ubyte    ),
    ]


PyCodeObject_p = ctypes.POINTER(PyCodeObject)


###


from ... import FlagGroup


class COFLAGS(FlagGroup):

    # Masks for co_flags above

    def __str__(self):
        return f'CO_{self._name_}'

    OPTIMIZED               = (  1 <<   0 )
    NEWLOCALS               = (  1 <<   1 )
    VARARGS                 = (  1 <<   2 )
    VARKEYWORDS             = (  1 <<   3 )
    NESTED                  = (  1 <<   4 )
    GENERATOR               = (  1 <<   5 )

    # The CO_NOFREE flag is set if there are no free or cell variables.
    # This information is redundant, but it allows a single flag test
    # to determine whether there is any extra work to be done when the
    # call frame it setup.
    NOFREE                  = (  1 <<   6 )

    # The CO_COROUTINE flag is set for coroutine functions (defined with
    # ``async def`` keywords)
    COROUTINE               = (  1 <<   7 )
    ITERABLE_COROUTINE      = (  1 <<   8 )
    ASYNC_GENERATOR         = (  1 <<   9 )

    # bpo-39562: These constant values are changed in Python 3.9
    # to prevent collision with compiler flags. CO_FUTURE_ and PyCF_
    # constants must be kept unique. PyCF_ constants can use bits from
    # 0x0100 to 0x10000. CO_FUTURE_ constants use bits starting at 0x20000.

    FUTURE_DIVISION         = (  2 <<  16 )
    FUTURE_ABSOLUTE_IMPORT  = (  2 <<  17 ) # do absolute imports by default

    FUTURE_WITH_STATEMENT   = (  2 <<  18 )
    FUTURE_PRINT_FUNCTION   = (  2 <<  19 )
    FUTURE_UNICODE_LITERALS = (  2 <<  20 )

    FUTURE_BARRY_AS_BDFL    = (  2 <<  21 )
    FUTURE_GENERATOR_STOP   = (  2 <<  22 )
    FUTURE_ANNOTATIONS      = (  2 <<  23 )

    # This value is found in the co_cell2arg array when the associated cell
    # variable does not correspond to an argument.
    CELL_NOT_AN_ARG         = ( -1 <<   0 )

    # Max static block nesting within a function
    MAXBLOCKS               = (  5 <<   2 )


###


from ..object import PyTypeObject


PyAPI_DATA("PyCode_Type",
    dtype = PyTypeObject,
    )


###


from ..object import Py_IS_TYPE
from .tupleobject import PyTuple_GET_SIZE


def PyCode_Check(op):
    """
    #define PyCode_Check(op) Py_IS_TYPE(op, &PyCode_Type)
    """
    return Py_IS_TYPE(op, PyCode_Type)


def PyCode_GetNumFree(op: PyCodeObject):
    """
    #define PyCode_GetNumFree(op) (PyTuple_GET_SIZE((op)->co_freevars))
    """
    return PyTuple_GET_SIZE(op.co_freevars)


### Public interface


PyAPI_FUNC("PyCode_New",
    restype = PyCodeObject_p,
    argtypes = [
        ctypes.c_int,
        ctypes.c_int,
        ctypes.c_int,
        ctypes.c_int,
        ctypes.c_int,
        PyObject_p,
        PyObject_p,
        PyObject_p,
        PyObject_p,
        PyObject_p,
        PyObject_p,
        PyObject_p,
        PyObject_p,
        ctypes.c_int,
        PyObject_p,
    ])

PyAPI_FUNC("PyCode_NewWithPosOnlyArgs",
    restype = PyCodeObject_p,
    argtypes = [
        ctypes.c_int,
        ctypes.c_int,
        ctypes.c_int,
        ctypes.c_int,
        ctypes.c_int,
        ctypes.c_int,
        PyObject_p,
        PyObject_p,
        PyObject_p,
        PyObject_p,
        PyObject_p,
        PyObject_p,
        PyObject_p,
        PyObject_p,
        ctypes.c_int,
        PyObject_p,
    ])

# Creates a new empty code object with the specified source location.
PyAPI_FUNC("PyCode_NewEmpty",
    restype = PyCodeObject_p,
    argtypes = [
        ctypes.c_char_p,
        ctypes.c_char_p,
        ctypes.c_int,
    ])

# Return the line number associated with the specified bytecode index
# in this code object.  If you just need the line number of a frame,
# use PyFrame_GetLineNumber() instead.
PyAPI_FUNC("PyCode_Addr2Line",
    restype = ctypes.c_int,
    argtypes = [
        PyCodeObject_p,
        ctypes.c_int,
    ])


###


class PyAddrPair(ctypes.Structure):
    """
    int ap_lower;
    int ap_upper;
    """

    # for internal use only

    _fields_ = [
        ('ap_lower' , ctypes.c_int ),
        ('ap_upper' , ctypes.c_int ),
    ]


PyAddrPair_p = ctypes.POINTER(PyAddrPair)


###


# Update *bounds to describe the first and one-past-the-last instructions in
# the same line as lasti.  Return the number of that line.
PyAPI_FUNC("_PyCode_CheckLineNumber",
    restype = ctypes.c_int,
    argtypes = [
        PyCodeObject_p,
        ctypes.c_int,
        PyAddrPair_p,
    ])

# Create a comparable key used to compare constants taking in account the
# object type. It is used to make sure types are not coerced (e.g., float and
# complex) _and_ to distinguish 0.0 from -0.0 e.g. on IEEE platforms
# Return (type(obj), obj, ...): a tuple with variable size (at least 2 items)
# depending on the type and the value. The type is the first item to not
# compare bytes and str which can raise a BytesWarning exception.
PyAPI_FUNC("_PyCode_ConstantKey",
    restype = PyObject_p,
    argtypes = [
        PyObject_p,
    ])

PyAPI_FUNC("PyCode_Optimize",
    restype = PyObject_p,
    argtypes = [
        PyObject_p,
        PyObject_p,
        PyObject_p,
        PyObject_p,
    ])

PyAPI_FUNC("_PyCode_GetExtra",
    restype = ctypes.c_int,
    argtypes = [
        PyObject_p,
        ctypes.py_ssize_t,
        ctypes.c_void_pp,
    ])

PyAPI_FUNC("_PyCode_SetExtra",
    restype = ctypes.c_int,
    argtypes = [
        PyObject_p,
        ctypes.py_ssize_t,
        ctypes.c_void_p,
    ])
