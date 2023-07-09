"""
Objects are structures allocated on the heap.  Special rules apply to
the use of objects to ensure they are properly garbage-collected.
Objects are never allocated statically or on the stack; they must be
accessed through special macros and functions only.  (Type objects are
exceptions to the first rule; the standard types are represented by
statically initialized type objects, although work on type/class unification
for Python 2.2 made it possible to have heap-allocated type objects too).

An object has a 'reference count' that is increased or decreased when a
pointer to the object is copied or deleted; when the reference count
reaches zero there are no references to the object left and it can be
removed from the heap.

An object has a 'type' that determines what it represents and what kind
of data it contains.  An object's type is fixed when it is created.
Types themselves are represented as objects; an object contains a
pointer to the corresponding type object.  The type itself has a type
pointer pointing to the object representing the type 'type', which
contains a pointer to itself!.

Objects do not float around in memory; once allocated an object keeps
the same size and address.  Objects that must hold variable-size data
can contain pointers to variable-size parts of the object.  Not all
objects of the same type have the same size; but the size cannot change
after allocation.  (These restrictions are made so a reference to an
object can be simply a pointer -- moving an object would require
updating all the pointers, and changing an object's size would require
moving it if there was another object right next to it.)

Objects are always accessed through pointers of the type 'PyObject *'.
The type 'PyObject' is a structure that only contains the reference count
and the type pointer.  The actual memory allocated for an object
contains other data that can only be accessed after casting the pointer
to a pointer to a longer structure type.  This longer type must start
with the reference count and type fields; the macro PyObject_HEAD should be
used for this (to accommodate for future changes).  The implementation
of a particular object type can cast the object pointer to the proper
type and back.

A standard interface exists for objects that contain an array of items
whose size is determined when the object is allocated.
"""

__all__ = [
    'unaryfunc', 'binaryfunc', 'ternaryfunc',
    'inquiry', 'lenfunc', 'ssizeargfunc', 'ssizessizeargfunc',
    'ssizeobjargproc', 'ssizessizeobjargproc', 'objobjargproc', 'objobjproc',
    'visitproc', 'traverseproc', 'freefunc', 'destructor',
    'getattrfunc', 'getattrofunc', 'setattrfunc', 'setattrofunc',
    'reprfunc', 'hashfunc', 'richcmpfunc', 'getiterfunc', 'iternextfunc',
    'descrgetfunc', 'descrsetfunc', 'initproc', 'newfunc', 'allocfunc',
    'PyTypeObject', 'PyTypeObject_p',
    '_PyObject_HEAD_EXTRA', '_PyObject_EXTRA_INIT',
    'PyObject', 'PyObject_p', 'PyObject_pp', 'PyObject_HEAD',
    'PyObject_HEAD_INIT', '_PyObject_CAST',
    'PyVarObject', 'PyVarObject_p', 'PyObject_VAR_HEAD',
    'PyVarObject_HEAD_INIT', '_PyVarObject_CAST',
    'Py_INVALID_SIZE', 'Py_REFCNT', 'Py_TYPE', 'Py_SIZE', 'Py_IS_TYPE',
    'Py_SET_REFCNT', 'Py_SET_TYPE', 'Py_SET_SIZE',
    'PyType_Slot', 'PyType_Slot_p', 'PyType_Spec', 'PyType_Spec_p',
    'PyObject_TypeCheck',
    'TPFLAGS', 'TPFLAG',
    'Py_LT', 'Py_LE', 'Py_EQ', 'Py_NE', 'Py_GT', 'Py_GE',
    'PyType_HasFeature', 'PyType_FastSubclass',
    'PyType_Check', 'PyType_CheckExact',
]


import _ctypes
import ctypes
import sys

from .. import PyAPI_DATA, PyAPI_FUNC


###


"""
Type objects contain a string containing the type name (to help somewhat
in debugging), the allocation parameters (see PyObject_New() and
PyObject_NewVar()),
and methods for accessing objects of the type.  Methods are optional, a
nil pointer meaning that particular kind of access is not available for
this type.  The Py_DECREF() macro uses the tp_dealloc method without
checking for a nil pointer; it should always be implemented except if
the implementation can guarantee that the reference count will never
reach zero (e.g., for statically allocated type objects).

NB: the methods for certain type groups are now contained in separate
method blocks.
"""


###


unaryfunc = ctypes.CFUNCTYPE(
    ctypes.py_object,
    ctypes.py_object,
    )

binaryfunc = ctypes.CFUNCTYPE(
    ctypes.py_object,
    ctypes.py_object, ctypes.py_object,
    )

ternaryfunc = ctypes.CFUNCTYPE(
    ctypes.py_object,
    ctypes.py_object, ctypes.py_object, ctypes.py_object,
    )

inquiry = ctypes.CFUNCTYPE(
    ctypes.c_int,
    ctypes.py_object,
    )

lenfunc = ctypes.CFUNCTYPE(
    ctypes.py_ssize_t,
    ctypes.py_object,
    )

ssizeargfunc = ctypes.CFUNCTYPE(
    ctypes.py_object,
    ctypes.py_object, ctypes.py_ssize_t,
    )

ssizessizeargfunc = ctypes.CFUNCTYPE(
    ctypes.py_object,
    ctypes.py_object, ctypes.py_ssize_t, ctypes.py_ssize_t,
    )

ssizeobjargproc = ctypes.CFUNCTYPE(
    ctypes.c_int,
    ctypes.py_object, ctypes.py_ssize_t, ctypes.py_object,
    )

ssizessizeobjargproc = ctypes.CFUNCTYPE(
    ctypes.c_int,
    ctypes.py_object, ctypes.py_ssize_t, ctypes.py_ssize_t, ctypes.py_object,
    )

objobjargproc = ctypes.CFUNCTYPE(
    ctypes.c_int,
    ctypes.py_object, ctypes.py_object, ctypes.py_object,
    )


###


objobjproc = ctypes.CFUNCTYPE(
    ctypes.c_int,
    ctypes.py_object, ctypes.py_object,
    )

visitproc = ctypes.CFUNCTYPE(
    ctypes.c_int,
    ctypes.py_object, ctypes.c_void_p,
    )

traverseproc = ctypes.CFUNCTYPE(
    ctypes.c_int,
    ctypes.py_object, visitproc, ctypes.c_void_p,
    )


###


freefunc = ctypes.CFUNCTYPE(
    None,
    ctypes.c_void_p,
    )

destructor = ctypes.CFUNCTYPE(
    None,
    ctypes.py_object
    )

getattrfunc = ctypes.CFUNCTYPE(
    ctypes.py_object,
    ctypes.py_object, ctypes.c_char_p,
    )

getattrofunc = ctypes.CFUNCTYPE(
    ctypes.py_object,
    ctypes.py_object, ctypes.py_object,
    )

setattrfunc = ctypes.CFUNCTYPE(
    ctypes.c_int,
    ctypes.py_object, ctypes.c_char_p, ctypes.py_object,
    )

setattrofunc = ctypes.CFUNCTYPE(
    ctypes.c_int,
    ctypes.py_object, ctypes.py_object, ctypes.py_object,
    )

reprfunc = ctypes.CFUNCTYPE(
    ctypes.py_object,
    ctypes.py_object,
    )

hashfunc = ctypes.CFUNCTYPE(
    ctypes.py_hash_t,
    ctypes.py_object,
    )

richcmpfunc = ctypes.CFUNCTYPE(
    ctypes.py_object,
    ctypes.py_object, ctypes.py_object, ctypes.c_int,
    )

getiterfunc = ctypes.CFUNCTYPE(
    ctypes.py_object,
    ctypes.py_object,
    )

iternextfunc = ctypes.CFUNCTYPE(
    ctypes.py_object,
    ctypes.py_object,
    )

descrgetfunc = ctypes.CFUNCTYPE(
    ctypes.py_object,
    ctypes.py_object, ctypes.py_object, ctypes.py_object,
    )

descrsetfunc = ctypes.CFUNCTYPE(
    ctypes.c_int,
    ctypes.py_object, ctypes.py_object, ctypes.py_object,
    )

initproc = ctypes.CFUNCTYPE(
    ctypes.c_int,
    ctypes.py_object, ctypes.py_object, ctypes.py_object,
    )

newfunc = ctypes.CFUNCTYPE(
    ctypes.py_object,
    ctypes.py_object, ctypes.py_object, ctypes.py_object,
    )

allocfunc = ctypes.CFUNCTYPE(
    ctypes.py_object,
    ctypes.py_object, ctypes.py_ssize_t,
    )


###


class PyTypeObject(ctypes.Structure): # _typeobject
    ...


PyTypeObject_p = ctypes.POINTER(PyTypeObject)


###


if ctypes.pyconfig.Py_TRACE_REFS:
    # Define pointers to support a doubly-linked list of all live heap objects
    _PyObject_HEAD_EXTRA = (
        ('_ob_next' , ctypes.py_object ),
        ('_ob_prev' , ctypes.py_object ),
    )
    _PyObject_EXTRA_INIT = (0, 0)
else:
    _PyObject_HEAD_EXTRA = ()
    _PyObject_EXTRA_INIT = ()


class PyObject(ctypes.Structure):
    """
    _PyObject_HEAD_EXTRA
    Py_ssize_t ob_refcnt;
    PyTypeObject *ob_type;
    """

    _fields_ = [
        *_PyObject_HEAD_EXTRA,
        ('ob_refcnt' , ctypes.py_ssize_t ),
        ('ob_type'   , PyTypeObject_p    ),
    ]

    @property
    def value(self):
        return _ctypes.PyObj_FromPtr(ctypes.addressof(self))


PyObject_p = ctypes.POINTER(PyObject)
PyObject_pp = ctypes.POINTER(PyObject_p)
PyObject_HEAD = (
    ('ob_base' , PyObject ),
)


def PyObject_HEAD_INIT(typ: PyTypeObject) -> PyObject:
    """
    #define PyObject_HEAD_INIT(type)        \
        { _PyObject_EXTRA_INIT              \
        1, type },
    """
    return PyObject(*_PyObject_EXTRA_INIT, 1, ctypes.pointer(typ))


def _PyObject_CAST(op):
    """
    /* Cast argument to PyObject* type. */
    #define _PyObject_CAST(op) ((PyObject*)(op))
    """
    ptr = ctypes.cast(ctypes.byref(op), PyObject_p)
    return ptr.contents


###


class PyVarObject(ctypes.Structure):
    """
    PyObject ob_base;
    Py_ssize_t ob_size;
    """

    _anonymous_ = ('ob_base',)
    _fields_ = [
        ('ob_base' , PyObject          ),
        # Number of items in variable part
        ('ob_size' , ctypes.py_hash_t  ), # XXX: py_hash_t / py_ssize_t ?
    ]


PyVarObject_p = ctypes.POINTER(PyVarObject)
PyObject_VAR_HEAD = (
    ('ob_base' , PyVarObject ),
)


def PyVarObject_HEAD_INIT(typ: PyTypeObject, size: ctypes.py_ssize_t):
    """
    /* Cast argument to PyVarObject* type. */
    #define PyVarObject_HEAD_INIT(type, size)       \
        { PyObject_HEAD_INIT(type) size },
    """
    return PyVarObject(*PyObject_HEAD_INIT(typ), size)


def _PyVarObject_CAST(op):
    """
    #define _PyVarObject_CAST(op) ((PyVarObject*)(op))
    """
    ptr = ctypes.cast(ctypes.byref(op), PyVarObject_p)
    return ptr.contents


###


Py_INVALID_SIZE = ctypes.py_ssize_t(-1)


def Py_REFCNT(ob) -> int:
    """
    #define Py_REFCNT(ob)           (_PyObject_CAST(ob)->ob_refcnt)
    """
    return _PyObject_CAST(ob).ob_refcnt


def Py_TYPE(ob) -> PyTypeObject:
    """
    #define Py_TYPE(ob)             (_PyObject_CAST(ob)->ob_type)
    """
    return _PyObject_CAST(ob).ob_type.contents


def Py_SIZE(ob) -> int:
    """
    #define Py_SIZE(ob)             (_PyVarObject_CAST(ob)->ob_size)
    """
    return _PyVarObject_CAST(ob).ob_size


def Py_IS_TYPE(ob, typ: PyTypeObject) -> bool:
    """
    static inline int _Py_IS_TYPE(const PyObject *ob, const PyTypeObject *type) {
        return ob->ob_type == type;
    }
    #define Py_IS_TYPE(ob, type) _Py_IS_TYPE(_PyObject_CAST_CONST(ob), type)
    """
    return ctypes.addressof(Py_TYPE(ob)) == ctypes.addressof(typ)


def Py_SET_REFCNT(ob, refcnt: int):
    """
    static inline void _Py_SET_REFCNT(PyObject *ob, Py_ssize_t refcnt) {
        ob->ob_refcnt = refcnt;
    }
    #define Py_SET_REFCNT(ob, refcnt) _Py_SET_REFCNT(_PyObject_CAST(ob), refcnt)
    """
    ob = _PyObject_CAST(ob)
    ob.ob_refcnt = refcnt


def Py_SET_TYPE(ob, typ: PyTypeObject):
    """
    static inline void _Py_SET_TYPE(PyObject *ob, PyTypeObject *type) {
        ob->ob_type = type;
    }
    #define Py_SET_TYPE(ob, type) _Py_SET_TYPE(_PyObject_CAST(ob), type)
    """
    ob = _PyObject_CAST(ob)
    ob.ob_type = ctypes.pointer(typ)


def Py_SET_SIZE(ob, size: int):
    """
    static inline void _Py_SET_SIZE(PyVarObject *ob, Py_ssize_t size) {
        ob->ob_size = size;
    }
    #define Py_SET_SIZE(ob, size) _Py_SET_SIZE(_PyVarObject_CAST(ob), size)
    """
    ob = _PyObject_CAST(ob)
    ob.ob_size = size


###


from .cpython.object import _typeobject


PyTypeObject._anonymous_ = ('_',)
PyTypeObject._fields_ = [
    ('_' , _typeobject ),
]


###


class PyType_Slot(ctypes.Structure):
    """
    int slot;
    void *pfunc;
    """

    _fields_ = [
        ('slot'  , ctypes.c_int    ), # slot id, see below
        ('pfunc' , ctypes.c_void_p ), # function pointer
    ]


PyType_Slot_p = ctypes.POINTER(PyType_Slot)


###


class PyType_Spec(ctypes.Structure):
    """
    const char* name;
    int basicsize;
    int itemsize;
    unsigned int flags;
    PyType_Slot *slots;
    """

    _fields_ = [
        ('name'      , ctypes.c_char_p ),
        ('basicsize' , ctypes.c_int    ),
        ('itemsize'  , ctypes.c_int    ),
        ('flags'     , ctypes.c_uint   ),
        ('slots'     , PyType_Slot_p   ), # terminated by slot==0.
    ]

PyType_Spec_p = ctypes.POINTER(PyType_Spec)


###


PyAPI_FUNC("PyType_FromSpec",
    restype = PyObject_p,
    argtypes = [
        PyType_Spec_p,
    ])


if sys.version_info >= (3, 3):
    PyAPI_FUNC("PyType_FromSpecWithBases",
        restype = PyObject_p,
        argtypes = [
            PyType_Spec_p,
            PyObject_p,
        ])


if sys.version_info >= (3, 4):
    PyAPI_FUNC("PyType_GetSlot",
        restype = ctypes.c_void_p,
        argtypes = [
            PyTypeObject_p,
            ctypes.c_int,
        ])


if sys.version_info >= (3, 9):
    PyAPI_FUNC("PyType_FromModuleAndSpec",
        restype = PyObject_p,
        argtypes = [
            PyObject_p,
            PyType_Spec_p,
            PyObject_p,
        ])

    PyAPI_FUNC("PyType_GetModule",
        restype = PyObject_p,
        argtypes = [
            PyTypeObject_p,
        ])

    PyAPI_FUNC("PyType_GetModuleState",
        restype = ctypes.c_void_p,
        argtypes = [
            PyTypeObject_p,
        ])


###


# Generic type check
PyAPI_FUNC("PyType_IsSubtype",
    restype = ctypes.c_bool,
    argtypes = [
        PyTypeObject_p,
        PyTypeObject_p,
    ])


def PyObject_TypeCheck(ob, tp):
    """
    #define PyObject_TypeCheck(ob, tp) \
        (Py_IS_TYPE(ob, tp) || PyType_IsSubtype(Py_TYPE(ob), (tp)))
    """
    return (
        Py_IS_TYPE(ob, tp)
        or PyType_IsSubtype(Py_TYPE(ob), tp)
        )


###


# built-in 'type'
PyAPI_DATA("PyType_Type",
    dtype = PyTypeObject,
    )

# built-in 'object'
PyAPI_DATA("PyBaseObject_Type",
    dtype = PyTypeObject,
    )

# built-in 'super'
PyAPI_DATA("PySuper_Type",
    dtype = PyTypeObject,
    )

PyAPI_FUNC("PyType_GetFlags",
    restype = ctypes.c_ulong,
    argtypes = [
        PyTypeObject_p,
    ])

PyAPI_FUNC("PyType_Ready",
    restype = ctypes.c_int,
    argtypes = [
        PyTypeObject_p,
    ])

PyAPI_FUNC("PyType_GenericAlloc",
    restype = PyObject_p,
    argtypes = [
        PyTypeObject_p,
        ctypes.py_ssize_t,
    ])

PyAPI_FUNC("PyType_GenericNew",
    restype = PyObject_p,
    argtypes = [
        PyTypeObject_p,
        PyObject_p,
        PyObject_p,
    ])

PyAPI_FUNC("PyType_ClearCache",
    restype = ctypes.c_uint,
    )

PyAPI_FUNC("PyType_Modified",
    argtypes = [
        PyTypeObject_p,
    ])


### Generic operations on objects


PyAPI_FUNC("PyObject_Repr",
    restype = PyObject_p,
    argtypes = [
        PyObject_p,
    ])

PyAPI_FUNC("PyObject_Str",
    restype = PyObject_p,
    argtypes = [
        PyObject_p,
    ])

PyAPI_FUNC("PyObject_ASCII",
    restype = PyObject_p,
    argtypes = [
        PyObject_p,
    ])

PyAPI_FUNC("PyObject_Bytes",
    restype = PyObject_p,
    argtypes = [
        PyObject_p,
    ])

PyAPI_FUNC("PyObject_RichCompare",
    restype = PyObject_p,
    argtypes = [
        PyObject_p,
        PyObject_p,
        ctypes.c_int,
    ])

PyAPI_FUNC("PyObject_RichCompareBool",
    restype = ctypes.c_int,
    argtypes = [
        PyObject_p,
        PyObject_p,
        ctypes.c_int,
    ])

PyAPI_FUNC("PyObject_GetAttrString",
    restype = PyObject_p,
    argtypes = [
        PyObject_p,
        ctypes.c_char_p,
    ])

PyAPI_FUNC("PyObject_SetAttrString",
    restype = ctypes.c_int,
    argtypes = [
        PyObject_p,
        ctypes.c_char_p,
        PyObject_p,
    ])

PyAPI_FUNC("PyObject_HasAttrString",
    restype = ctypes.c_int,
    argtypes = [
        PyObject_p,
        ctypes.c_char_p,
    ])

PyAPI_FUNC("PyObject_GetAttr",
    restype = PyObject_p,
    argtypes = [
        PyObject_p,
        PyObject_p,
    ])

PyAPI_FUNC("PyObject_SetAttr",
    restype = ctypes.c_int,
    argtypes = [
        PyObject_p,
        PyObject_p,
        PyObject_p,
    ])

PyAPI_FUNC("PyObject_HasAttr",
    restype = ctypes.c_int,
    argtypes = [
        PyObject_p,
        PyObject_p,
    ])

PyAPI_FUNC("PyObject_SelfIter",
    restype = PyObject_p,
    argtypes = [
        PyObject_p,
    ])

PyAPI_FUNC("PyObject_GenericGetAttr",
    restype = PyObject_p,
    argtypes = [
        PyObject_p,
        PyObject_p,
    ])

PyAPI_FUNC("PyObject_GenericSetAttr",
    restype = ctypes.c_int,
    argtypes = [
        PyObject_p,
        PyObject_p,
        PyObject_p,
    ])


if sys.version_info >= (3, 3):
    PyAPI_FUNC("PyObject_GenericSetDict",
        restype = ctypes.c_int,
        argtypes = [
            PyObject_p,
            PyObject_p,
            ctypes.c_void_p,
        ])


PyAPI_FUNC("PyObject_Hash",
    restype = ctypes.py_hash_t,
    argtypes = [
        PyObject_p,
    ])

PyAPI_FUNC("PyObject_HashNotImplemented",
    restype = ctypes.py_hash_t,
    argtypes = [
        PyObject_p,
    ])

PyAPI_FUNC("PyObject_IsTrue",
    restype = ctypes.c_int,
    argtypes = [
        PyObject_p,
    ])

PyAPI_FUNC("PyObject_Not",
    restype = ctypes.c_int,
    argtypes = [
        PyObject_p,
    ])

PyAPI_FUNC("PyCallable_Check",
    restype = ctypes.c_int,
    argtypes = [
        PyObject_p,
    ])

PyAPI_FUNC("PyObject_ClearWeakRefs",
    argtypes = [
        PyObject_p,
    ])

# PyObject_Dir(obj) acts like Python builtins.dir(obj), returning a
# list of strings.  PyObject_Dir(NULL) is like builtins.dir(),
# returning the names of the current locals.  In this case, if there are
# no current locals, NULL is returned, and PyErr_Occurred() is false.
PyAPI_FUNC("PyObject_Dir",
    restype = PyObject_p,
    argtypes = [
        PyObject_p,
    ])

# Helpers for printing recursive container types

PyAPI_FUNC("Py_ReprEnter",
    restype = ctypes.c_int,
    argtypes = [
        PyObject_p,
    ])

PyAPI_FUNC("Py_ReprLeave",
    argtypes = [
        PyObject_p,
    ])


### Flag bits for printing:


# No string quotes etc.
Py_PRINT_RAW = 1


###


from .. import FlagGroup


class TPFLAGS(FlagGroup):
    """
    Type flags (tp_flags)

    These flags are used to change expected features and behavior for a
    particular type.

    Arbitration of the flag bit positions will need to be coordinated among
    all extension writers who publicly release their extensions (this will
    be fewer than you might expect!).

    Most flags were removed as of Python 3.0 to make room for new flags. (Some
    flags are not for backwards compatibility but to indicate the presence of
    an optional feature; these flags remain of course.)

    Type definitions should use Py_TPFLAGS_DEFAULT for their tp_flags value.

    Code can use PyType_HasFeature(type_ob, flag_value) to test whether the
    given type object has a specified feature.
    """

    def __str__(self):
        return f'Py_{self.__class__.__name__}_{self._name_}'

    # These flag bits were deprecated with v3.0.
    # HAVE_GETCHARBUFFER       = (  1 <<  0 )
    # HAVE_SEQUENCE_IN         = (  1 <<  1 )
    # GC                       = (  1 <<  2 )
    # HAVE_INPLACEOPS          = (  1 <<  3 )
    # CHECKTYPES               = (  1 <<  4 )
    # HAVE_RICHCOMPARE         = (  1 <<  5 )
    # HAVE_WEAKREFS            = (  1 <<  6 )
    # HAVE_ITER                = (  1 <<  7 )
    # HAVE_CLASS               = (  1 <<  8 )

    # Set if the type object is dynamically allocated
    HEAPTYPE                 = (  1 <<  9 )

    # Set if the type allows subclassing
    BASETYPE                 = (  1 << 10 )

    # Set if the type implements the vectorcall protocol (PEP 590)
    HAVE_VECTORCALL          = (  1 << 11 )

    # Set if the type is 'ready' -- fully initialized
    READY                    = (  1 << 12 )

    # Set while the type is being 'readied', to prevent recursive ready calls
    READYING                 = (  1 << 13 )

    # Objects support garbage collection
    HAVE_GC                  = (  1 << 14 )

    # Two bits are preserved for Stackless Python
    HAVE_STACKLESS_EXTENSION = (  3 << 15 )

    # Objects behave like an unbound method
    METHOD_DESCRIPTOR        = (  1 << 17 )

    # Objects support type attribute cache
    HAVE_VERSION_TAG         = (  1 << 18 )
    VALID_VERSION_TAG        = (  1 << 19 )

    # Type is abstract and cannot be instantiated
    IS_ABSTRACT              = (  1 << 20 )

    # These flags are used to determine if a type is a subclass.
    LONG_SUBCLASS            = (  1 << 24 )
    LIST_SUBCLASS            = (  1 << 25 )
    TUPLE_SUBCLASS           = (  1 << 26 )
    BYTES_SUBCLASS           = (  1 << 27 )
    UNICODE_SUBCLASS         = (  1 << 28 )
    DICT_SUBCLASS            = (  1 << 29 )
    BASE_EXC_SUBCLASS        = (  1 << 30 )
    TYPE_SUBCLASS            = (  1 << 31 )

    # The following flags reuse the lower bits that were removed in v3.0.

    # Type structure has tp_finalize member
    HAVE_FINALIZE            = (  1 <<  0 )

    # (HAVE_STACKLESS_EXTENSION | HAVE_VERSION_TAG | 0)
    DEFAULT                  = ( 11 << 15 )
    NONE                     = (  0 <<  0 )


TPFLAG = TPFLAGS._select


###


if ctypes.pyconfig.Py_REF_DEBUG:
    PyAPI_DATA("_Py_RefTotal",
        dtype = ctypes.py_ssize_t,
        )

    PyAPI_FUNC("_Py_NegativeRefcount",
        argtypes = [
            ctypes.c_char_p, # filename
            ctypes.c_int,    # lineno
            PyObject_p,      # op
        ])


PyAPI_FUNC("_Py_Dealloc",
    argtypes = [
        PyObject_p,
    ])


###

# These are provided as conveniences to Python runtime embedders, so that
# they can have object code that is not dependent on Python compilation flags.

PyAPI_FUNC("Py_IncRef",
    argtypes = [
        PyObject_p,
    ])

PyAPI_FUNC("Py_DecRef",
    argtypes = [
        PyObject_p,
    ])


###


PyAPI_DATA("_Py_NoneStruct",
    dtype = PyObject,
    )

PyAPI_DATA("_Py_NotImplementedStruct",
    dtype = PyObject,
    )


###


Py_LT = 0
Py_LE = 1
Py_EQ = 2
Py_NE = 3
Py_GT = 4
Py_GE = 5


###


def PyType_HasFeature(tp: PyTypeObject, feature: int) -> int:
    """
    static inline int
    PyType_HasFeature(PyTypeObject *type, unsigned long feature)
    {
        unsigned long flags;
    #ifdef Py_LIMITED_API
        // PyTypeObject is opaque in the limited C API
        flags = PyType_GetFlags(type);
    #else
        flags = type->tp_flags;
    #endif
        return ((flags & feature) != 0);
    }
    """
    if ctypes.pyconfig.Py_LIMITED_API:
        flags = PyType_GetFlags(tp)
    else:
        flags = tp.tp_flags

    return ((flags & feature) != 0)


def PyType_FastSubclass(tp, flag):
    """
    #define PyType_FastSubclass(type, flag) PyType_HasFeature(type, flag)
    """
    return PyType_HasFeature(tp, flag)


def PyType_Check(op):
    """
    static inline int _PyType_Check(PyObject *op) {
        return PyType_FastSubclass(Py_TYPE(op), Py_TPFLAGS_TYPE_SUBCLASS);
    }
    #define PyType_Check(op) _PyType_Check(_PyObject_CAST(op))
    """
    op = _PyObject_CAST(op)
    return PyType_FastSubclass(Py_TYPE(op), TPFLAG('TYPE_SUBCLASS'))


def PyType_CheckExact(op):
    """
    static inline int _PyType_CheckExact(PyObject *op) {
        return Py_IS_TYPE(op, &PyType_Type);
    }
    #define PyType_CheckExact(op) _PyType_CheckExact(_PyObject_CAST(op))
    """
    op = _PyObject_CAST(op)
    return Py_IS_TYPE(op, PyType_Type)
