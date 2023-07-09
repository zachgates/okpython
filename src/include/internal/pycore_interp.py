__all__ = [
    '_pending_calls', '_pending_calls_p',
    '_ceval_state', '_ceval_state_p',
    '_Py_unicode_fs_codec', '_Py_unicode_fs_codec_p',
    '_Py_unicode_state', '_Py_unicode_state_p',
    '_xidregitem', '_xidregitem_p',
    '_PY_NSMALLPOSINTS', '_PY_NSMALLNEGINTS', '_is', '_is_p',
]


import ctypes


###


from ..pythread import PyThread_type_lock
from .pycore_atomic import _Py_atomic_int


class _pending_calls(ctypes.Structure):
    """
    PyThread_type_lock lock;
    _Py_atomic_int calls_to_do;
    int async_exc;
    struct {
        int (*func)(void *);
        void *arg;
    } calls[NPENDINGCALLS];
    int first;
    int last;
    """

    NPENDINGCALLS = 32

    class calls(ctypes.Structure):
        """
        int (*func)(void *);
        void *arg;
        """

        _fields_ = [
            ('func' , ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_void_p) ),
            ('arg'  , ctypes.c_void_p                                 ),
        ]

    _fields_ = [
        ('lock'        , PyThread_type_lock                 ),

        # Request for running pending calls.
        ('calls_to_do' , _Py_atomic_int                     ),

        # Request for looking at the `async_exc` field of the current
        # thread state. Guarded by the GIL.
        ('async_exc'   , ctypes.c_int                       ),

        ('calls'       , ctypes.ARRAY(calls, NPENDINGCALLS) ),

        ('first'       , ctypes.c_int                       ),
        ('last'        , ctypes.c_int                       ),
    ]


_pending_calls_p = ctypes.POINTER(_pending_calls)


###


class _ceval_state(ctypes.Structure):
    """
    int recursion_limit;
    int tracing_possible;
    _Py_atomic_int eval_breaker;
    _Py_atomic_int gil_drop_request;
    struct _pending_calls pending;
    """

    _fields_ = [
        ('recursion_limit'  , ctypes.c_int   ),

        # Records whether tracing is on for any thread.
        # Counts the number of threads for which `tstate->c_tracefunc` is
        # non-NULL, so if the value is 0, we know we don't have to check this
        # thread's `c_tracefunc`. This speeds up the if statement in
        # `_PyEval_EvalFrameDefault()` after `fast_next_opcode`.
        ('tracing_possible' , ctypes.c_int   ),

        # This single variable consolidates all requests to break out of
        # the fast path in the eval loop.
        ('eval_breaker'     , _Py_atomic_int ),

        # Request for dropping the GIL
        ('gil_drop_request' , _Py_atomic_int ),
        ('pending'          , _pending_calls ),
    ]


_ceval_state_p = ctypes.POINTER(_ceval_state)


###


class _Py_unicode_fs_codec(ctypes.Structure):
    """
    char *encoding;
    int utf8;
    char *errors;
    _Py_error_handler error_handler;
    """

    _fields_ = [
        # Filesystem encoding (encoded to UTF-8)
        ('encoding'      , ctypes.c_char_p   ),

        # encoding=="utf-8"?
        ('utf8'          , ctypes.c_int      ),

        # Filesystem errors (encoded to UTF-8)
        ('errors'        , ctypes.c_char_p   ),
        ('error_handler' , ctypes.c_int      ),
    ]


_Py_unicode_fs_codec_p = ctypes.POINTER(_Py_unicode_fs_codec)


###


class _Py_unicode_state(ctypes.Structure):
    """
    struct _Py_unicode_fs_codec fs_codec;
    """

    # `fs_codec.encoding` is initialized to NULL.
    # Later, it is set to a non-NULL string by `_PyUnicode_InitEncodings()`.

    _fields_ = [
        ('fs_codec' , _Py_unicode_fs_codec ),
    ]


_Py_unicode_state_p = ctypes.POINTER(_Py_unicode_state)


### cross-interpreter data registry


from ..object import PyTypeObject_p
from ..cpython.pystate import crossinterpdatafunc


class _xidregitem(ctypes.Structure):
    """
    PyTypeObject *cls;
    crossinterpdatafunc getdata;
    struct _xidregitem *next;
    """


_xidregitem_p = ctypes.POINTER(_xidregitem)
_xidregitem._fields_ = [
    ('cls'     , PyTypeObject_p      ),
    ('getdata' , crossinterpdatafunc ),
    ('next'    , _xidregitem_p       ),
]


###


from .pycore_gc import _gc_runtime_state
from .pycore_runtime import _PyRuntimeState_p
from ..pythread import PyThread_type_lock
from ..object import freefunc, destructor
from ..longintrepr import PyLongObject_p
from ..cpython.pystate import _PyFrameEvalFunction
from ..cpython.initconfig import PyConfig


_PY_NSMALLPOSINTS = 257
_PY_NSMALLNEGINTS = 5


class _is(ctypes.Structure):
    """
    struct _is *next;
    struct _ts *tstate_head;
    struct pyruntimestate *runtime;
    int64_t id;
    int64_t id_refcount;
    int requires_idref;
    PyThread_type_lock id_mutex;
    int finalizing;
    struct _ceval_state ceval;
    struct _gc_runtime_state gc;
    PyObject *modules;
    PyObject *modules_by_index;
    PyObject *sysdict;
    PyObject *builtins;
    PyObject *importlib;
    long num_threads;
    size_t pythread_stacksize;
    PyObject *codec_search_path;
    PyObject *codec_search_cache;
    PyObject *codec_error_registry;
    int codecs_initialized;
    struct _Py_unicode_state unicode;
    PyConfig config;
#ifdef HAVE_DLOPEN
    int dlopenflags;
#endif
    PyObject *dict;
    PyObject *builtins_copy;
    PyObject *import_func;
    _PyFrameEvalFunction eval_frame;
    Py_ssize_t co_extra_user_count;
    freefunc co_extra_freefuncs[MAX_CO_EXTRA_USERS];
#ifdef HAVE_FORK
    PyObject *before_forkers;
    PyObject *after_forkers_parent;
    PyObject *after_forkers_child;
#endif
    void (*pyexitfunc)(PyObject *);
    PyObject *pyexitmodule;
    uint64_t tstate_next_unique_id;
    struct _warnings_runtime_state warnings;
    PyObject *audit_hooks;
    struct {
        struct {
            int level;
            int atbol;
        } listnode;
    } parser;
#if _PY_NSMALLNEGINTS + _PY_NSMALLPOSINTS > 0
    PyLongObject* small_ints[_PY_NSMALLNEGINTS + _PY_NSMALLPOSINTS];
#endif
    """

    # The PyInterpreterState typedef is in Include/pystate.h.

    class parser(ctypes.Structure):
        """
        struct {
            struct {
                int level;
                int atbol;
            } listnode;
        } parser;
        """

        class listnode(ctypes.Structure):
            """
            struct {
                int level;
                int atbol;
            } listnode;
            """

            _fields_ = [
                ('level' , ctypes.c_int ),
                ('atbol' , ctypes.c_int ),
            ]

        _fields_ = [
            ('listnode' , listnode ),
        ]


_is_p = ctypes.POINTER(_is)
_is._fields_ = [
    ('next'                      , _is_p                    ),
    ('tstate_head'               , _is_p                    ),

    # Reference to the _PyRuntime global variable. This field exists
    # to not have to pass runtime in addition to tstate to a function.
    # Get runtime from tstate: tstate->interp->runtime.
    ('runtime'                   , _PyRuntimeState_p        ),

    ('id'                        , ctypes.c_int64           ),
    ('id_refcount'               , ctypes.c_int64           ),
    ('requires_idref'            , ctypes.c_int             ),
    ('id_mutex'                  , PyThread_type_lock       ),

    ('finalizing'                , ctypes.c_int             ),

    ('ceval'                     , _ceval_state             ),
    ('gc'                        , _gc_runtime_state        ),

    ('modules'                   , ctypes.py_object         ),
    ('modules_by_index'          , ctypes.py_object         ),
    ('sysdict'                   , ctypes.py_object         ),
    ('builtins'                  , ctypes.py_object         ),
    ('importlib'                 , ctypes.py_object         ),

    ('num_threads'               , ctypes.c_long            ),
    # A value of 0 means using the platform's default stack size
    # or the size specified by the THREAD_STACK_SIZE macro.
    ('pythread_stacksize'        , ctypes.c_size_t          ),

    ('codec_search_path'         , ctypes.py_object         ),
    ('codec_search_cache'        , ctypes.py_object         ),
    ('codec_error_registry'      , ctypes.py_object         ),
    ('codecs_initialized'        , ctypes.c_int             ),

    ('unicode'                   , _Py_unicode_state        ),

    ('config'                    , PyConfig                 ),
    *(
        (('dlopenflags'          , ctypes.c_int             ),
         )
        if ctypes.pyconfig.HAVE_DLOPEN
        else ()
    ),

    # Stores per-interpreter state
    ('dict'                      , ctypes.py_object         ),

    ('builtins_copy'             , ctypes.py_object         ),
    ('import_func'               , ctypes.py_object         ),

    # Initialized to `PyEval_EvalFrameDefault()`.
    ('eval_frame'                , _PyFrameEvalFunction     ),

    ('co_extra_user_count'       , ctypes.py_ssize_t        ),
    ('co_extra_freefuncs'        , freefunc                 ),

    *(
        (('before_forkers'       , ctypes.py_object         ),
         ('after_forkers_parent' , ctypes.py_object         ),
         ('after_forkers_child'  , ctypes.py_object         ),
         )
        if ctypes.pyconfig.HAVE_FORK
        else ()
    ),

    # AtExit module
    ('pyexitfunc'                , destructor               ),
    ('pyexitmodule'              , ctypes.py_object         ),

    ('tstate_next_unique_id'     , ctypes.c_uint64          ),

    ('warnings'                  , ctypes.c_void_p          ), # _warnings_runtime_state

    ('audit_hooks'               , ctypes.py_object         ),

    ('parser'                    , _is.parser               ),

    # Small integers are preallocated in this array so that they can be
    # shared. The integers that are preallocated are those in the range
    # -_PY_NSMALLNEGINTS (inclusive) to _PY_NSMALLPOSINTS (not inclusive).
    *(
        (('small_ints'           , ctypes.ARRAY(
                                       PyLongObject_p,
                                       _PY_NSMALLNEGINTS
                                       + _PY_NSMALLPOSINTS) ),
         )
        if _PY_NSMALLNEGINTS + _PY_NSMALLPOSINTS > 0
        else ()
    ),
]
