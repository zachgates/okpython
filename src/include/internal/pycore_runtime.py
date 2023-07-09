__all__ = [
    '_ceval_runtime_state', '_ceval_runtime_state_p',
    '_gilstate_runtime_state', '_gilstate_runtime_state_p',
    '_Py_AuditHookEntry', '_Py_AuditHookEntry_p',
    '_PyRuntimeState', '_PyRuntimeState_p',
]


import ctypes

from .pycore_atomic import _Py_atomic_address


###


from .pycore_atomic import _Py_atomic_int
from .pycore_gil import _gil_runtime_state


class _ceval_runtime_state(ctypes.Structure):
    """
    _Py_atomic_int signals_pending;
    struct _gil_runtime_state gil;
    """

    _fields_ = [
        ('signals_pending' , _Py_atomic_int ),
        ('gil'             , _gil_runtime_state ),
    ]


_ceval_runtime_state_p = ctypes.POINTER(_ceval_runtime_state)


###


# from ..pystate import PyInterpreterState_p
from ..pythread import Py_tss_t


class _gilstate_runtime_state(ctypes.Structure):
    """
    int check_enabled;
    _Py_atomic_address tstate_current;
    PyInterpreterState *autoInterpreterState;
    Py_tss_t autoTSSkey;
    """

    _fields_ = [
        ('check_enabled'        , ctypes.c_int         ),
        ('tstate_current'       , _Py_atomic_address   ),
        ('autoInterpreterState' , ctypes.c_void_p      ), # PyInterpreterState_p
        ('autoTSSkey'           , Py_tss_t             ),
    ]


_gilstate_runtime_state_p = ctypes.POINTER(_gilstate_runtime_state)


###


from ..cpython.sysmodule import Py_AuditHookFunction


class _Py_AuditHookEntry(ctypes.Structure):
    """
    struct _Py_AuditHookEntry *next;
    Py_AuditHookFunction hookCFunction;
    void *userData;
    """


_Py_AuditHookEntry_p = ctypes.POINTER(_Py_AuditHookEntry)
_Py_AuditHookEntry._fields_ = [
    ('next'          , _Py_AuditHookEntry_p ),
    ('hookCFunction' , Py_AuditHookFunction ),
    ('userData'      , ctypes.c_void_p      ),
]


###


from .pycore_interp import _xidregitem_p
from ..pythread import PyThread_type_lock
from ..cpython.initconfig import PyPreConfig
from ..cpython.fileobject import Py_OpenCodeHookFunction


class _PyRuntimeState(ctypes.Structure):
    """
    int preinitializing;
    int preinitialized;
    int core_initialized;
    int initialized;
    _Py_atomic_address _finalizing;
    struct pyinterpreters {
        PyThread_type_lock mutex;
        PyInterpreterState *head;
        PyInterpreterState *main;
        int64_t next_id;
    } interpreters;
    """

    NEXITFUNCS = 32

    class pyinterpreters(ctypes.Structure):
        """
        struct pyinterpreters {
            PyThread_type_lock mutex;
            PyInterpreterState *head;
            PyInterpreterState *main;
            int64_t next_id;
        } interpreters;
        """

        _fields_ = [
            ('mutex'   , PyThread_type_lock   ),
            ('head'    , ctypes.c_void_p      ), # PyInterpreterState_p
            ('main'    , ctypes.c_void_p      ), # PyInterpreterState_p
            ('next_id' , ctypes.c_int64       ),
        ]

    class _xidregistry(ctypes.Structure):
        """
        struct _xidregistry {
            PyThread_type_lock mutex;
            struct _xidregitem *head;
        } xidregistry;
        """

        _fields_ = [
            ('mutex' , PyThread_type_lock ),
            ('head'  , _xidregitem_p      ),
        ]

    _fields_ = [
        # Is running Py_PreInitialize()?
        ('preinitializing'    , ctypes.c_int                ),
        # Is Python preinitialized? Set to 1 by Py_PreInitialize()
        ('preinitialized'     , ctypes.c_int                ),
        # Is Python core initialized? Set to 1 by _Py_InitializeCore()
        ('core_initialized'   , ctypes.c_int                ),
        # Is Python fully initialized? Set to 1 by Py_Initialize()
        ('initialized'        , ctypes.c_int                ),

        # Set by Py_FinalizeEx(). Only reset to NULL if Py_Initialize()
        # is called again.
        #
        # Use _PyRuntimeState_GetFinalizing() and
        # _PyRuntimeState_SetFinalizing() to access it,
        # don't access it directly.
        ('_finalizing'        , _Py_atomic_address          ),

        ('interpreters'       , pyinterpreters              ),

        # XXX Remove this field once we have a tp_* slot.
        ('xidregistry'        , _xidregistry                ),

        ('main_thread'        , ctypes.c_ulong              ),

        ('exitfuncs'          , ctypes.ARRAY(
                                    ctypes.CFUNCTYPE(None),
                                    NEXITFUNCS,
                                    )                       ),
        ('nexitfuncs'         , ctypes.c_int                ),

        ('ceval'              , _ceval_runtime_state        ),
        ('gilstate'           , _gilstate_runtime_state     ),

        ('preconfig'          , PyPreConfig                 ),

        ('open_code_hook'     , Py_OpenCodeHookFunction     ),
        ('open_code_userdata' , ctypes.c_void_p             ),
        ('audit_hook_head'    , _Py_AuditHookEntry_p        ),
    ]


_PyRuntimeState_p = ctypes.POINTER(_PyRuntimeState)
