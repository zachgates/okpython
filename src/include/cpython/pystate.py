__all__ = [
    'Py_tracefunc', 'PyTrace',
    '_PyErr_StackItem', '_PyErr_StackItem_p',
    '_PyCrossInterpreterData', '_PyCrossInterpreterData_p',
    'crossinterpdatafunc',
    '_ts', '_ts_p',
    '_PyFrameEvalFunction',
]


import ctypes

from ... import PyAPI_FUNC
from ..object import freefunc, PyObject_p
from ..pyframe import PyFrameObject_p


###


PyAPI_FUNC("_PyInterpreterState_RequiresIDRef",
    restype = ctypes.c_int,
    argtypes = [
        ctypes.c_void_p, # PyInterpreterState *
    ])

PyAPI_FUNC("_PyInterpreterState_RequireIDRef",
    argtypes = [
        ctypes.c_void_p, # PyInterpreterState *
        ctypes.c_int,
    ])

PyAPI_FUNC("_PyInterpreterState_GetMainModule",
    restype = PyObject_p,
    argtypes = [
        ctypes.c_void_p, # PyInterpreterState *
    ])


###


# Py_tracefunc return -1 when raising an exception, or 0 for success.
Py_tracefunc = ctypes.CFUNCTYPE(
    ctypes.c_int,
    ctypes.py_object, PyFrameObject_p, ctypes.c_int, ctypes.py_object,
    )


###


from ... import FlagGroup


class PyTrace(FlagGroup):
    """
    The following values are used for 'what' for tracefunc functions
    To add a new kind of trace event, also update "trace_init" in
    Python/sysmodule.c to define the Python level event name
    """

    def __str__(self):
        return f'{self.__class__.__name__}_{self._name_}'

    CALL        = 0
    EXCEPTION   = 1
    LINE        = 2
    RETURN      = 3
    C_CALL      = 4
    C_EXCEPTION = 5
    C_RETURN    = 6
    OPCODE      = 7


###


class _PyErr_StackItem(ctypes.Structure):
    """
    PyObject *exc_type, *exc_value, *exc_traceback;
    struct _err_stackitem *previous_item;
    """

    # This struct represents an entry on the exception stack, which is a
    # per-coroutine state. (Coroutine in the computer science sense,
    # including the thread and generators).
    # This ensures that the exception state is not impacted by "yields"
    # from an except handler.


_PyErr_StackItem_p = ctypes.POINTER(_PyErr_StackItem)
_PyErr_StackItem._fields_ = [
    ('exc_type'      , ctypes.py_object   ),
    ('exc_value'     , ctypes.py_object   ),
    ('exc_traceback' , ctypes.py_object   ),
    ('previous_item' , _PyErr_StackItem_p ),
]


###


class _PyCrossInterpreterData(ctypes.Structure):
    """
    void *data;
    PyObject *obj;
    int64_t interp;
    PyObject *(*new_object)(struct _xid *);
    void (*free)(void *);
    """

    # _PyCrossInterpreterData is similar to Py_buffer as an effectively
    # opaque struct that holds data outside the object machinery.  This
    # is necessary to pass safely between interpreters in the same process.


_PyCrossInterpreterData_p = ctypes.POINTER(_PyCrossInterpreterData)
_PyCrossInterpreterData._fields_ = [
    ('data'       , ctypes.c_void_p                ),
    ('obj'        , ctypes.py_object               ),
    ('interp'     , ctypes.c_int64                 ),
    ('new_object' , ctypes.CFUNCTYPE(
                        ctypes.py_object,
                        _PyCrossInterpreterData_p,
                        )                          ),
    ('free'       , freefunc                       ),
]


###


PyAPI_FUNC("_PyObject_GetCrossInterpreterData",
    restype = ctypes.c_int,
    argtypes = [
        PyObject_p,
        _PyCrossInterpreterData_p,
    ])

PyAPI_FUNC("_PyCrossInterpreterData_NewObject",
    restype = PyObject_p,
    argtypes = [
        _PyCrossInterpreterData_p,
    ])

PyAPI_FUNC("_PyCrossInterpreterData_Release",
    argtypes = [
        _PyCrossInterpreterData_p,
    ])

PyAPI_FUNC("_PyObject_CheckCrossInterpreterData",
    restype = ctypes.c_int,
    argtypes = [
        PyObject_p,
    ])


###


crossinterpdatafunc = ctypes.CFUNCTYPE(
    ctypes.c_int,
    ctypes.py_object, _PyCrossInterpreterData_p,
    )


###


from ..object import PyTypeObject_p


PyAPI_FUNC("_PyCrossInterpreterData_RegisterClass",
    restype = ctypes.c_int,
    argtypes = [
        PyTypeObject_p,
        crossinterpdatafunc,
    ])

PyAPI_FUNC("_PyCrossInterpreterData_Lookup",
    restype = crossinterpdatafunc,
    argtypes = [
        PyObject_p,
    ])


###


class _ts(ctypes.Structure):
    """
    struct _ts *prev;
    struct _ts *next;
    PyInterpreterState *interp;

    PyFrameObject *frame;
    int recursion_depth;
    char overflowed;
    char recursion_critical;
    int stackcheck_counter;

    int tracing;
    int use_tracing;

    Py_tracefunc c_profilefunc;
    Py_tracefunc c_tracefunc;
    PyObject *c_profileobj;
    PyObject *c_traceobj;

    PyObject *curexc_type;
    PyObject *curexc_value;
    PyObject *curexc_traceback;

    _PyErr_StackItem exc_state;
    _PyErr_StackItem *exc_info;

    PyObject *dict;

    int gilstate_counter;

    PyObject *async_exc;
    unsigned long thread_id;

    int trash_delete_nesting;
    PyObject *trash_delete_later;

    void (*on_delete)(void *);
    void *on_delete_data;

    int coroutine_origin_tracking_depth;

    PyObject *async_gen_firstiter;
    PyObject *async_gen_finalizer;

    PyObject *context;
    uint64_t context_ver;

    uint64_t id;
    """

    # See Python/ceval.c for comments explaining most fields


_ts_p = ctypes.POINTER(_ts)
_ts._fields_ = [
    ('prev'                            , _ts_p                ),
    ('next'                            , _ts_p                ),
    ('interp'                          , ctypes.c_void_p      ), # _is_p

    # Borrowed reference to the current frame (it can be NULL)
    ('frame'                           , PyFrameObject_p      ),
    ('recursion_depth'                 , ctypes.c_int         ),
    # The stack has overflowed. Allow 50 more calls to handle
    # the runtime error.
    ('overflowed'                      , ctypes.c_char        ),
    # The current calls must not cause a stack overflow.
    ('recursion_critical'              , ctypes.c_char        ),
    ('stackcheck_counter'              , ctypes.c_int         ),

    # 'tracing' keeps track of the execution depth when tracing/profiling.
    # This is to prevent the actual trace/profile code from being recorded in
    # the trace/profile.
    ('tracing'                         , ctypes.c_int         ),
    ('use_tracing'                     , ctypes.c_int         ),

    ('c_profilefunc'                   , Py_tracefunc         ),
    ('c_tracefunc'                     , Py_tracefunc         ),
    ('c_profileobj'                    , ctypes.py_object     ),
    ('c_traceobj'                      , ctypes.py_object     ),

    # The exception currently being raised
    ('curexc_type'                     , ctypes.py_object     ),
    ('curexc_value'                    , ctypes.py_object     ),
    ('curexc_traceback'                , ctypes.py_object     ),

    # The exception currently being handled, if no coroutines/generators
    # are present. Always last element on the stack referred to be exc_info.
    ('exc_state'                       , _PyErr_StackItem     ),

    # Pointer to the top of the stack of the exceptions currently
    # being handled
    ('exc_info'                        , _PyErr_StackItem_p   ),

    # Stores per-thread state
    ('dict'                            , ctypes.py_object     ),

    ('gilstate_counter'                , ctypes.c_int         ),

    # Asynchronous exception to raise
    ('async_exc'                       , ctypes.py_object     ),
    # Thread id where this tstate was created
    ('thread_id'                       , ctypes.c_ulong       ),

    ('trash_delete_nesting'            , ctypes.c_int         ),
    ('trash_delete_later'              , ctypes.py_object     ),

    ('on_delete'                       , freefunc ),
    ('on_delete_data'                  , ctypes.c_void_p      ),

    ('coroutine_origin_tracking_depth' , ctypes.c_int         ),

    ('async_gen_firstiter'             , ctypes.py_object     ),
    ('async_gen_finalizer'             , ctypes.py_object     ),

    ('context'                         , ctypes.py_object     ),
    ('context_ver'                     , ctypes.c_uint64      ),

    # Unique thread state id.
    ('id'                              , ctypes.c_uint64      ),
]


###


PyAPI_FUNC("_PyThreadState_Prealloc",
    restype = _ts_p,
    argtypes = [
        ctypes.c_void_p, # PyInterpreterState *
    ])

PyAPI_FUNC("_PyThreadState_UncheckedGet",
    restype = _ts_p,
    )

PyAPI_FUNC("_PyThreadState_GetDict",
    restype = PyObject_p,
    argtypes = [
        _ts_p,
    ])

PyAPI_FUNC("PyGILState_Check",
    restype = ctypes.c_int,
    )

PyAPI_FUNC("_PyGILState_GetInterpreterStateUnsafe",
    restype = ctypes.c_void_p, # PyInterpreterState *
    )

PyAPI_FUNC("_PyThread_CurrentFrames",
    restype = PyObject_p,
    )

PyAPI_FUNC("PyInterpreterState_Main",
    restype = ctypes.c_void_p, # PyInterpreterState *
    )

PyAPI_FUNC("PyInterpreterState_Head",
    restype = ctypes.c_void_p, # PyInterpreterState *
    )

PyAPI_FUNC("PyInterpreterState_Next",
    restype = ctypes.c_void_p, # PyInterpreterState *
    argtypes = [
        ctypes.c_void_p, # PyInterpreterState *
    ])

PyAPI_FUNC("PyInterpreterState_ThreadHead",
    restype = _ts_p,
    argtypes = [
        ctypes.c_void_p, # PyInterpreterState *
    ])

PyAPI_FUNC("PyThreadState_Next",
    restype = _ts_p,
    argtypes = [
        _ts_p,
    ])

PyAPI_FUNC("PyThreadState_DeleteCurrent",
    )


###


_PyFrameEvalFunction = ctypes.CFUNCTYPE(
    ctypes.py_object,
    _ts_p, PyFrameObject_p, ctypes.c_int,
    )


###


PyAPI_FUNC("_PyInterpreterState_GetEvalFrameFunc",
    restype = _PyFrameEvalFunction,
    argtypes = [
        ctypes.c_void_p, # PyInterpreterState *
    ])

PyAPI_FUNC("_PyInterpreterState_SetEvalFrameFunc",
    argtypes = [
        ctypes.c_void_p, # PyInterpreterState *
        _PyFrameEvalFunction,
    ])

PyAPI_FUNC("_PyInterpreterState_GetConfig",
    restype = ctypes.c_void_p, # PyConfig *
    argtypes = [
        ctypes.c_void_p, # PyInterpreterState *
    ])

PyAPI_FUNC("_Py_GetConfig",
    restype = ctypes.c_void_p, # PyConfig *
    )
