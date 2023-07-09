__all__ = [
    'PyTryBlock', 'PyTryBlock_p',
    '_frame', '_frame_p',
]


import ctypes


###


class PyTryBlock(ctypes.Structure):
    """
    int b_type;
    int b_handler;
    int b_level;
    """

    _fields_ = [
        # what kind of block this is
        ('b_type'    , ctypes.c_int ),
        # where to jump to find handler
        ('b_handler' , ctypes.c_int ),
        # value stack level to pop to
        ('b_level'   , ctypes.c_int ),
    ]


PyTryBlock_p = ctypes.POINTER(PyTryBlock)


###


from ..object import PyObject_VAR_HEAD
from .code import PyCodeObject_p


class _frame(ctypes.Structure):
    """
    PyObject_VAR_HEAD
    struct _frame *f_back;
    PyCodeObject *f_code;
    PyObject *f_builtins;
    PyObject *f_globals;
    PyObject *f_locals;
    PyObject **f_valuestack;
    PyObject **f_stacktop;
    PyObject *f_trace;
    char f_trace_lines;
    char f_trace_opcodes;
    PyObject *f_gen;
    int f_lasti;
    int f_lineno;
    int f_iblock;
    char f_executing;
    PyTryBlock f_blockstack[CO_MAXBLOCKS];
    PyObject *f_localsplus[1];
    """


_frame_p = ctypes.POINTER(_frame)
_frame._fields_ = [
    *PyObject_VAR_HEAD,
    # previous frame, or NULL
    ('f_back'          , _frame_p           ),
    # code segment
    ('f_code'          , PyCodeObject_p     ),
    # builtin symbol table (PyDictObject)
    ('f_builtins'      , ctypes.py_object   ),
    # global symbol table (PyDictObject)
    ('f_globals'       , ctypes.py_object   ),
    # local symbol table (any mapping)
    ('f_locals'        , ctypes.py_object   ),
    # points after the last local
    ('f_valuestack'    , ctypes.py_object_p ),
    # Next free slot in f_valuestack.  Frame creation sets to f_valuestack.
    # Frame evaluation usually NULLs it, but a frame that yields sets it
    # to the current stack top.
    ('f_stacktop'      , ctypes.py_object_p ),
    # Trace function
    ('f_trace'         , ctypes.py_object   ),
    # Emit per-line trace events?
    ('f_trace_lines'   , ctypes.c_char      ),
    # Emit per-opcode trace events?
    ('f_trace_opcodes' , ctypes.c_char      ),
    # Borrowed reference to a generator, or NULL
    ('f_gen'           , ctypes.py_object   ),
    # Last instruction if called
    ('f_lasti'         , ctypes.c_int       ),
    # Current line number
    # Call PyFrame_GetLineNumber() instead of reading this field directly.
    ('f_lineno'        , ctypes.c_int       ),
    # index in f_blockstack
    ('f_iblock'        , ctypes.c_int       ),
    # whether the frame is still executing
    ('f_executing'     , ctypes.c_char      ),
    # for try and loop blocks
    ('f_blockstack'    , PyTryBlock_p       ),
    # locals+stack, dynamically sized
    ('f_localsplus'    , ctypes.py_object_p ),
]


###


from ... import PyAPI_DATA, PyAPI_FUNC
from ..object import PyTypeObject, PyObject_p
from .code import PyCodeObject_p


PyAPI_DATA("PyFrame_Type",
    dtype = PyTypeObject,
    )

PyAPI_FUNC("PyFrame_New",
    restype = _frame_p,
    argtypes = [
        ctypes.c_void_p, # PyThreadState_p
        PyCodeObject_p,
        PyObject_p,
        PyObject_p,
    ])


# The rest of the interface is specific for frame objects


# Block management functions

PyAPI_FUNC("PyFrame_BlockSetup",
    argtypes = [
        _frame_p,
        ctypes.c_int,
        ctypes.c_int,
        ctypes.c_int,
    ])

PyAPI_FUNC("PyFrame_BlockPop",
    restype = PyTryBlock_p,
    argtypes = [
        _frame_p
    ])

# Conversions between "fast locals" and locals in dictionary

PyAPI_FUNC("PyFrame_LocalsToFast",
    argtypes = [
        _frame_p,
        ctypes.c_int,
    ])

PyAPI_FUNC("PyFrame_FastToLocalsWithError",
    restype = ctypes.c_int,
    argtypes = [
        _frame_p, # f
    ])

PyAPI_FUNC("PyFrame_FastToLocals",
    argtypes = [
        _frame_p,
    ])

PyAPI_FUNC("_PyFrame_DebugMallocStats",
    argtypes = [
        ctypes.c_void_p, # FILE *out
    ])

PyAPI_FUNC("PyFrame_GetBack",
    restype = _frame_p,
    argtypes = [
        _frame_p, # frame
    ])
