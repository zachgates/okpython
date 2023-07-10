__all__ = [
    '_Py_Identifier', '_Py_Identifier_p',
    # '_Py_static_string_init', '_Py_static_string', '_Py_IDENTIFIER',
    'bufferinfo', 'Py_buffer', 'Py_buffer_p',
    'getbufferproc', 'releasebufferproc', 'vectorcallfunc',
    'PyBUF_MAX_NDIM', 'PyBUF_READ', 'PyBUF_WRITE', 'PyBUF',
    'PyNumberMethods', 'PyNumberMethods_p',
    'PySequenceMethods', 'PySequenceMethods_p',
    'PyMappingMethods', 'PyMappingMethods_p',
    'PyAsyncMethods', 'PyAsyncMethods_p',
    'PyBufferProcs', 'PyBufferProcs_p',
    'printfunc',
    '_typeobject', '_typeobject_p',
    'PyHeapTypeObject', 'PyHeapTypeObject_p',
    'PyTrash_UNWIND_LEVEL',
]


import ctypes
import sys

from ... import PyAPI_DATA, PyAPI_FUNC
from ..object import PyObject_p, PyObject_pp


###


PyAPI_FUNC("_Py_NewReference",
    argtypes = [
        PyObject_p,
    ])


if ctypes.pyconfig.Py_TRACE_REFS:
    PyAPI_FUNC("_Py_ForgetReference",
        argtypes = [
            PyObject_p,
        ])


# PyAPI_FUNC("_PyTraceMalloc_NewReference",
#     restype = ctypes.c_int,
#     argtypes = [
#         PyObject_p,
#     ])


if ctypes.pyconfig.Py_DEBUG:
    PyAPI_FUNC("_Py_GetRefTotal",
        restype = ctypes.py_ssize_t,
        )


###


import textwrap


class _Py_Identifier(ctypes.Structure):
    """
    struct _Py_Identifier *next;
    const char* string;
    PyObject *object;
    """


_Py_Identifier_p = ctypes.POINTER(_Py_Identifier)
_Py_Identifier._fields_ = [
    ('next'   , _Py_Identifier_p ),
    ('string' , ctypes.c_char_p  ),
    ('object' , ctypes.py_object ),
]


# def _Py_static_string_init(value: str):
#     return _Py_Identifier(string = value.encode())
#
#
# def _Py_static_string(varname: str, value: str):
#     exec(textwrap.dedent(
#         f'''
#         global {varname}
#         {varname} = _Py_static_string_init(value)
#         '''
#         ))
#
#
# def _Py_IDENTIFIER(varname: str):
#     _Py_static_string(f'PyId_{varname}', varname)


### buffer interface


from ... import FlagGroup


class bufferinfo(ctypes.Structure):
    """
    void *buf;
    PyObject *obj;
    Py_ssize_t len;
    Py_ssize_t itemsize;
    int readonly;
    int ndim;
    char *format;
    Py_ssize_t *shape;
    Py_ssize_t *strides;
    Py_ssize_t *suboffsets;
    void *internal;
    """

    _fields_ = [
        ('buf'        , ctypes.c_void_p   ),
        ('obj'        , ctypes.py_object  ), # owned reference
        ('len'        , ctypes.py_ssize_t ),
        # This is Py_ssize_t so it can be pointed to by strides
        # in a simple case.
        ('itemsize'   , ctypes.py_ssize_t ),
        ('readonly'   , ctypes.c_int      ),
        ('ndim'       , ctypes.c_int      ),
        ('format'     , ctypes.c_char_p   ),
        ('shape'      , ctypes.py_ssize_t ),
        ('strides'    , ctypes.py_ssize_t ),
        ('suboffsets' , ctypes.py_ssize_t ),
        ('internal'   , ctypes.c_void_p   ),
    ]


class Py_buffer(bufferinfo):
    pass


Py_buffer_p = ctypes.POINTER(Py_buffer)


###


getbufferproc = ctypes.CFUNCTYPE(
    ctypes.c_int,
    ctypes.py_object, Py_buffer_p, ctypes.c_int,
    )

releasebufferproc = ctypes.CFUNCTYPE(
    None,
    ctypes.py_object, Py_buffer_p,
    )

vectorcallfunc = ctypes.CFUNCTYPE(
    ctypes.py_object,
    ctypes.py_object, ctypes.py_object_p, ctypes.c_size_t, ctypes.py_object,
    )


###


PyBUF_MAX_NDIM = 64 # Maximum number of dimensions
PyBUF_READ     = 0x100
PyBUF_WRITE    = 0x200


class PyBUF(FlagGroup):

    """
    Flags for getting buffers
    """

    def __str__(self):
        return f'{self.__class__.__name__}_{self._name_}'

    SIMPLE         = 0
    WRITABLE       = 0x0001
    WRITEABLE      = WRITABLE
    FORMAT         = 0x0004
    ND             = 0x0008
    STRIDES        = (0x0010 | ND)
    C_CONTIGUOUS   = (0x0020 | STRIDES)
    F_CONTIGUOUS   = (0x0040 | STRIDES)
    ANY_CONTIGUOUS = (0x0080 | STRIDES)
    INDIRECT       = (0x0100 | STRIDES)
    CONTIG         = (ND | WRITABLE)
    CONTIG_RO      = (ND)
    STRIDED        = (STRIDES | WRITABLE)
    STRIDED_RO     = (STRIDES)
    RECORDS        = (STRIDES | WRITABLE | FORMAT)
    RECORDS_RO     = (STRIDES | FORMAT)
    FULL           = (INDIRECT | WRITABLE | FORMAT)
    FULL_RO        = (INDIRECT | FORMAT)


### End buffer interface


from ..object import unaryfunc, binaryfunc, ternaryfunc
from ..object import inquiry, lenfunc, ssizeargfunc, ssizeobjargproc
from ..object import objobjargproc, objobjproc
from ..object import destructor, getattrfunc, setattrfunc, reprfunc, hashfunc
from ..object import getattrofunc, setattrofunc, traverseproc, richcmpfunc
from ..object import getiterfunc, iternextfunc, descrgetfunc, descrsetfunc
from ..object import initproc, allocfunc, newfunc, freefunc


class PyNumberMethods(ctypes.Structure):
    """
    binaryfunc nb_add;
    binaryfunc nb_subtract;
    binaryfunc nb_multiply;
    binaryfunc nb_remainder;
    binaryfunc nb_divmod;
    ternaryfunc nb_power;
    unaryfunc nb_negative;
    unaryfunc nb_positive;
    unaryfunc nb_absolute;
    inquiry nb_bool;
    unaryfunc nb_invert;
    binaryfunc nb_lshift;
    binaryfunc nb_rshift;
    binaryfunc nb_and;
    binaryfunc nb_xor;
    binaryfunc nb_or;
    unaryfunc nb_int;
    void *nb_reserved;
    unaryfunc nb_float;

    binaryfunc nb_inplace_add;
    binaryfunc nb_inplace_subtract;
    binaryfunc nb_inplace_multiply;
    binaryfunc nb_inplace_remainder;
    ternaryfunc nb_inplace_power;
    binaryfunc nb_inplace_lshift;
    binaryfunc nb_inplace_rshift;
    binaryfunc nb_inplace_and;
    binaryfunc nb_inplace_xor;
    binaryfunc nb_inplace_or;

    binaryfunc nb_floor_divide;
    binaryfunc nb_true_divide;
    binaryfunc nb_inplace_floor_divide;
    binaryfunc nb_inplace_true_divide;

    unaryfunc nb_index;

    binaryfunc nb_matrix_multiply;
    binaryfunc nb_inplace_matrix_multiply;
    """

    # Number implementations must check *both*
    # arguments for proper type and implement the necessary conversions
    # in the slot functions themselves.

    _fields_ = [
        ('nb_add'                     , binaryfunc      ),
        ('nb_subtract'                , binaryfunc      ),
        ('nb_multiply'                , binaryfunc      ),
        ('nb_remainder'               , binaryfunc      ),
        ('nb_divmod'                  , binaryfunc      ),
        ('nb_power'                   , ternaryfunc     ),
        ('nb_negative'                , unaryfunc       ),
        ('nb_positive'                , unaryfunc       ),
        ('nb_absolute'                , unaryfunc       ),
        ('nb_bool'                    , inquiry         ), # nb_nonzero
        ('nb_invert'                  , unaryfunc       ),
        ('nb_lshift'                  , binaryfunc      ),
        ('nb_rshift'                  , binaryfunc      ),
        ('nb_and'                     , binaryfunc      ),
        ('nb_xor'                     , binaryfunc      ),
        ('nb_or'                      , binaryfunc      ),
        ('nb_int'                     , unaryfunc       ),
        ('nb_reserved'                , ctypes.c_void_p ), # nb_long
        ('nb_float'                   , unaryfunc       ),
        #
        ('nb_inplace_add'             , binaryfunc      ),
        ('nb_inplace_subtract'        , binaryfunc      ),
        ('nb_inplace_multiply'        , binaryfunc      ),
        ('nb_inplace_remainder'       , binaryfunc      ),
        ('nb_inplace_power'           , ternaryfunc     ),
        ('nb_inplace_lshift'          , binaryfunc      ),
        ('nb_inplace_rshift'          , binaryfunc      ),
        ('nb_inplace_and'             , binaryfunc      ),
        ('nb_inplace_xor'             , binaryfunc      ),
        ('nb_inplace_or'              , binaryfunc      ),
        #
        ('nb_floor_divide'            , binaryfunc      ),
        ('nb_true_divide'             , binaryfunc      ),
        ('nb_inplace_floor_divide'    , binaryfunc      ),
        ('nb_inplace_true_divide'     , binaryfunc      ),
        #
        ('nb_index'                   , unaryfunc       ),
        #
        ('nb_matrix_multiply'         , binaryfunc      ),
        ('nb_inplace_matrix_multiply' , binaryfunc      ),
    ]


PyNumberMethods_p = ctypes.POINTER(PyNumberMethods)


###


class PySequenceMethods(ctypes.Structure):
    """
    lenfunc sq_length;
    binaryfunc sq_concat;
    ssizeargfunc sq_repeat;
    ssizeargfunc sq_item;
    void *was_sq_slice;
    ssizeobjargproc sq_ass_item;
    void *was_sq_ass_slice;
    objobjproc sq_contains;

    binaryfunc sq_inplace_concat;
    ssizeargfunc sq_inplace_repeat;
    """

    _fields_ = [
        ('sq_length'         , lenfunc         ),
        ('sq_concat'         , binaryfunc      ),
        ('sq_repeat'         , ssizeargfunc    ),
        ('sq_item'           , ssizeargfunc    ),
        ('was_sq_slice'      , ctypes.c_void_p ),
        ('sq_ass_item'       , ssizeobjargproc ),
        ('was_sq_ass_slice'  , ctypes.c_void_p ),
        ('sq_contains'       , objobjproc      ),
        #
        ('sq_inplace_concat' , binaryfunc      ),
        ('sq_inplace_repeat' , ssizeargfunc    ),
    ]


PySequenceMethods_p = ctypes.POINTER(PySequenceMethods)


###


class PyMappingMethods(ctypes.Structure):
    """
    lenfunc mp_length;
    binaryfunc mp_subscript;
    objobjargproc mp_ass_subscript;
    """

    _fields_ = [
        ('mp_length'        , lenfunc       ),
        ('mp_subscript'     , binaryfunc    ),
        ('mp_ass_subscript' , objobjargproc ),
    ]


PyMappingMethods_p = ctypes.POINTER(PyMappingMethods)


###


class PyAsyncMethods(ctypes.Structure):
    """
    unaryfunc am_await;
    unaryfunc am_aiter;
    unaryfunc am_anext;
    """

    _fields_ = [
        ('am_await' , unaryfunc ),
        ('am_aiter' , unaryfunc ),
        ('am_anext' , unaryfunc ),
    ]


PyAsyncMethods_p = ctypes.POINTER(PyAsyncMethods)


###


class PyBufferProcs(ctypes.Structure):
    """
    getbufferproc bf_getbuffer;
    releasebufferproc bf_releasebuffer;
    """

    _fields_ = [
        ('bf_getbuffer'     , getbufferproc     ),
        ('bf_releasebuffer' , releasebufferproc ),
    ]


PyBufferProcs_p = ctypes.POINTER(PyBufferProcs)


###


# Allow printfunc in the tp_vectorcall_offset slot
# for backwards-compatibility
printfunc = ctypes.py_ssize_t


###


from ..object import PyObject_VAR_HEAD, PyTypeObject_p
from ..methodobject import PyMethodDef_p
from ..structmember import PyMemberDef_p
from ..descrobject import PyGetSetDef_p


class _typeobject(ctypes.Structure):
    """
    PyObject_VAR_HEAD
    const char *tp_name;
    Py_ssize_t tp_basicsize, tp_itemsize;

    destructor tp_dealloc;
    Py_ssize_t tp_vectorcall_offset;
    getattrfunc tp_getattr;
    setattrfunc tp_setattr;
    PyAsyncMethods *tp_as_async;
    reprfunc tp_repr;

    PyNumberMethods *tp_as_number;
    PySequenceMethods *tp_as_sequence;
    PyMappingMethods *tp_as_mapping;

    hashfunc tp_hash;
    ternaryfunc tp_call;
    reprfunc tp_str;
    getattrofunc tp_getattro;
    setattrofunc tp_setattro;

    PyBufferProcs *tp_as_buffer;

    unsigned long tp_flags;

    const char *tp_doc;

    traverseproc tp_traverse;

    inquiry tp_clear;

    richcmpfunc tp_richcompare;

    Py_ssize_t tp_weaklistoffset;

    getiterfunc tp_iter;
    iternextfunc tp_iternext;

    struct PyMethodDef *tp_methods;
    struct PyMemberDef *tp_members;
    struct PyGetSetDef *tp_getset;
    struct _typeobject *tp_base;
    PyObject *tp_dict;
    descrgetfunc tp_descr_get;
    descrsetfunc tp_descr_set;
    Py_ssize_t tp_dictoffset;
    initproc tp_init;
    allocfunc tp_alloc;
    newfunc tp_new;
    freefunc tp_free;
    inquiry tp_is_gc;
    PyObject *tp_bases;
    PyObject *tp_mro;
    PyObject *tp_cache;
    PyObject *tp_subclasses;
    PyObject *tp_weaklist;
    destructor tp_del;

    unsigned int tp_version_tag;

    destructor tp_finalize;
    vectorcallfunc tp_vectorcall;
    """

    _anonymous_ = ('ob_base',)
    _fields_ = [
        *PyObject_VAR_HEAD,

        # For printing, in format "<module>.<name>"
        ('tp_name'               , ctypes.c_char_p     ),

        # For allocation
        ('tp_basicsize'          , ctypes.py_ssize_t   ),
        ('tp_itemsize'           , ctypes.py_ssize_t   ),

        # Methods to implement standard operations
        ('tp_dealloc'            , destructor          ),
        ('tp_vectorcall_offset'  , ctypes.py_ssize_t   ), # tp_print
        ('tp_getattr'            , getattrfunc         ),
        ('tp_setattr'            , setattrfunc         ),
        # formerly known as tp_compare (Python 2) or tp_reserved (Python 3)
        ('tp_as_async'           , PyAsyncMethods_p    ),
        ('tp_repr'               , reprfunc            ),

        # Method suites for standard classes
        ('tp_as_number'          , PyNumberMethods_p   ),
        ('tp_as_sequence'        , PySequenceMethods_p ),
        ('tp_as_mapping'         , PyMappingMethods_p  ),

        # More standard operations (here for binary compatibility)
        ('tp_hash'               , hashfunc            ),
        ('tp_call'               , ternaryfunc         ),
        ('tp_str'                , reprfunc            ),
        ('tp_getattro'           , getattrofunc        ),
        ('tp_setattro'           , setattrofunc        ),

        # Functions to access object as input/output buffer
        ('tp_as_buffer'          , PyBufferProcs_p     ),

        # Flags to define presence of optional/expanded features
        ('tp_flags'              , ctypes.c_ulong      ),

        # Documentation string
        ('tp_doc'                , ctypes.c_char_p     ),

        # Assigned meaning in release 2.0
        # call function for all accessible objects
        ('tp_traverse'           , traverseproc        ),

        # delete references to contained objects
        ('tp_clear'              , inquiry             ),

        # Assigned meaning in release 2.1
        # rich comparisons
        ('tp_richcompare'        , richcmpfunc         ),

        # weak reference enabler
        ('tp_weaklistoffset'     , ctypes.py_ssize_t   ),

        # Iterators
        ('tp_iter'               , getiterfunc         ),
        ('tp_iternext'           , iternextfunc        ),

        # Attribute descriptor and subclassing stuff
        ('tp_methods'            , PyMethodDef_p       ),
        ('tp_members'            , PyMemberDef_p       ),
        ('tp_getset'             , PyGetSetDef_p       ),
        ('tp_base'               , PyTypeObject_p      ),
        ('tp_dict'               , ctypes.py_object    ),
        ('tp_descr_get'          , descrgetfunc        ),
        ('tp_descr_set'          , descrsetfunc        ),
        ('tp_dictoffset'         , ctypes.py_ssize_t   ),
        ('tp_init'               , initproc            ),
        ('tp_alloc'              , allocfunc           ),
        ('tp_new'                , newfunc             ),
        # Low-level free-memory routine
        ('tp_free'               , freefunc            ),
        # For PyObject_IS_GC
        ('tp_is_gc'              , inquiry             ),
        ('tp_bases'              , ctypes.py_object    ),
        # method resolution order
        ('tp_mro'                , ctypes.py_object    ),
        ('tp_cache'              , ctypes.py_object    ),
        ('tp_subclasses'         , ctypes.py_object    ),
        ('tp_weaklist'           , ctypes.py_object    ),
        ('tp_del'                , destructor          ),

        # Type attribute cache version tag. Added in version 2.6
        ('tp_version_tag'        , ctypes.c_uint       ),

        ('tp_finalize'           , destructor          ),
        ('tp_vectorcall'         , vectorcallfunc      ),
    ]


_typeobject_p = ctypes.POINTER(_typeobject)


###


from ...objects.dict_common import _dictkeysobject


class PyHeapTypeObject(ctypes.Structure):
    """
    PyTypeObject ht_type;
    PyAsyncMethods as_async;
    PyNumberMethods as_number;
    PyMappingMethods as_mapping;
    PySequenceMethods as_sequence;
    PyBufferProcs as_buffer;
    PyObject *ht_name, *ht_slots, *ht_qualname;
    struct _dictkeysobject *ht_cached_keys;
    PyObject *ht_module;
    """

    # The *real* layout of a type object when allocated on the heap

    _fields_ = [
        ('ht_type'        , _typeobject                     ),
        ('as_async'       , PyAsyncMethods                  ),
        ('as_number'      , PyNumberMethods                 ),
        ('as_mapping'     , PyMappingMethods                ),
        # as_sequence comes after as_mapping, so that the mapping wins when
        # both the mapping and the sequence define a given operator
        ('as_sequence'    , PySequenceMethods               ),
        ('as_buffer'      , PyBufferProcs                   ),
        ('ht_name'        , ctypes.py_object                ),
        ('ht_slots'       , ctypes.py_object                ),
        ('ht_qualname'    , ctypes.py_object                ),
        ('ht_cached_keys' , ctypes.POINTER(_dictkeysobject) ),
        ('ht_module'      , ctypes.py_object                ),
    ]


PyHeapTypeObject_p = ctypes.POINTER(PyHeapTypeObject)


###


PyAPI_FUNC("_PyType_Name",
    restype = ctypes.c_char_p,
    argtypes = [
        PyTypeObject_p,
    ])

PyAPI_FUNC("_PyType_Lookup",
    restype = PyObject_p,
    argtypes = [
        PyTypeObject_p,
        PyObject_p,
    ])

PyAPI_FUNC("_PyType_LookupId",
    restype = PyObject_p,
    argtypes = [
        PyTypeObject_p,
        _Py_Identifier_p,
    ])

PyAPI_FUNC("_PyObject_LookupSpecial",
    restype = PyObject_p,
    argtypes = [
        PyObject_p,
        _Py_Identifier_p,
    ])

PyAPI_FUNC("_PyType_CalculateMetaclass",
    restype = PyTypeObject_p,
    argtypes = [
        PyTypeObject_p,
        PyObject_p,
    ])

PyAPI_FUNC("_PyType_GetDocFromInternalDoc",
    restype = PyObject_p,
    argtypes = [
        ctypes.c_char_p,
        ctypes.c_char_p,
    ])

PyAPI_FUNC("_PyType_GetTextSignatureFromInternalDoc",
    restype = PyObject_p,
    argtypes = [
        ctypes.c_char_p,
        ctypes.c_char_p,
    ])

PyAPI_FUNC("PyObject_Print",
    restype = ctypes.c_int,
    argtypes = [
        PyObject_p,
        ctypes.c_void_p, # FILE *
        ctypes.c_int,
    ])

PyAPI_FUNC("_Py_BreakPoint",
    )

PyAPI_FUNC("_PyObject_Dump",
    argtypes = [
        PyObject_p,
    ])

PyAPI_FUNC("_PyObject_IsFreed",
    restype = ctypes.c_int,
    argtypes = [
        PyObject_p,
    ])

PyAPI_FUNC("_PyObject_IsAbstract",
    restype = ctypes.c_int,
    argtypes = [
        PyObject_p,
    ])

PyAPI_FUNC("_PyObject_GetAttrId",
    restype = PyObject_p,
    argtypes = [
        PyObject_p,
        _Py_Identifier_p,
    ])

PyAPI_FUNC("_PyObject_SetAttrId",
    restype = ctypes.c_int,
    argtypes = [
        PyObject_p,
        _Py_Identifier_p,
        PyObject_p,
    ])

# PyAPI_FUNC("_PyObject_HasAttrId",
#     restype = ctypes.c_int,
#     argtypes = [
#         PyObject_p,
#         _Py_Identifier_p,
#     ])

PyAPI_FUNC("_PyObject_LookupAttr",
    restype = ctypes.c_int,
    argtypes = [
        PyObject_p,
        PyObject_p,
        PyObject_pp,
    ])

PyAPI_FUNC("_PyObject_LookupAttrId",
    restype = ctypes.c_int,
    argtypes = [
        PyObject_p,
        _Py_Identifier_p,
        PyObject_pp,
    ])

PyAPI_FUNC("_PyObject_GetMethod",
    restype = ctypes.c_int,
    argtypes = [
        PyObject_p,
        PyObject_p,
        PyObject_pp,
    ])

PyAPI_FUNC("_PyObject_GetDictPtr",
    restype = PyObject_pp,
    argtypes = [
        PyObject_p,
    ])

PyAPI_FUNC("_PyObject_NextNotImplemented",
    restype = PyObject_p,
    argtypes = [
        PyObject_p,
    ])

PyAPI_FUNC("PyObject_CallFinalizer",
    argtypes = [
        PyObject_p,
    ])

PyAPI_FUNC("PyObject_CallFinalizerFromDealloc",
    restype = ctypes.c_int,
    argtypes = [
        PyObject_p,
    ])

PyAPI_FUNC("_PyObject_GenericGetAttrWithDict",
    restype = PyObject_p,
    argtypes = [
        PyObject_p,
        PyObject_p,
        PyObject_p,
        ctypes.c_int,
    ])

PyAPI_FUNC("_PyObject_GenericSetAttrWithDict",
    restype = ctypes.c_int,
    argtypes = [
        PyObject_p,
        PyObject_p,
        PyObject_p,
        PyObject_p,
    ])

PyAPI_FUNC("_PyObject_FunctionStr",
    restype = PyObject_p,
    argtypes = [
        PyObject_p,
    ])

PyAPI_DATA("_PyNone_Type",
    dtype = _typeobject,
    )

PyAPI_DATA("_PyNotImplemented_Type",
    dtype = _typeobject,
    )

PyAPI_DATA("_Py_SwappedOp",
    dtype = ctypes.c_int_p, # int[]
    )

PyAPI_FUNC("_PyDebugAllocatorStats",
    argtypes = [
        ctypes.c_void_p, # FILE *
        ctypes.c_char_p,
        ctypes.c_int,
        ctypes.c_size_t,
    ])

PyAPI_FUNC("_PyObject_DebugTypeStats",
    argtypes = [
        ctypes.c_void_p, # FILE *
    ])

PyAPI_FUNC("_PyObject_AssertFailed",
    argtypes = [
        PyObject_p,
        ctypes.c_char_p,
        ctypes.c_char_p,
        ctypes.c_char_p,
        ctypes.c_int,
        ctypes.c_char_p,
    ])

PyAPI_FUNC("_PyObject_CheckConsistency",
    restype = ctypes.c_int,
    argtypes = [
        PyObject_p,
        ctypes.c_int,
    ])

PyAPI_FUNC("_PyTrash_deposit_object",
    argtypes = [
        PyObject_p,
    ])

PyAPI_FUNC("_PyTrash_destroy_chain",
    )

PyAPI_FUNC("_PyTrash_thread_deposit_object",
    argtypes = [
        PyObject_p,
    ])

PyAPI_FUNC("_PyTrash_thread_destroy_chain",
    )

PyAPI_FUNC("_PyTrash_begin",
    restype = ctypes.c_int,
    argtypes = [
        ctypes.c_void_p, # PyThreadState *
        PyObject_p,
    ])

PyAPI_FUNC("_PyTrash_end",
    argtypes = [
        ctypes.c_void_p, # PyThreadState *
    ])

PyTrash_UNWIND_LEVEL = 50
