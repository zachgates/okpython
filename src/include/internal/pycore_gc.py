__all__ = [
    'PyGC_Head', 'PyGC_Head_p',
    'gc_generation', 'gc_generation_p',
    'gc_generation_stats', 'gc_generation_stats_p',
    'NUM_GENERATIONS', '_gc_runtime_state', '_gc_runtime_state_p',
]


import ctypes


###


class PyGC_Head(ctypes.Structure):
    """
    uintptr_t _gc_next;
    uintptr_t _gc_prev;
    """

    _fields_ = [
        # Pointer to next object in the list.
        # 0 means the object is not tracked
        ('_gc_next' , ctypes.c_void_p ),

        # Pointer to previous object in the list.
        # Lowest two bits are used for flags documented later.
        ('_gc_prev' , ctypes.c_void_p ),
    ]


PyGC_Head_p = ctypes.POINTER(PyGC_Head)


###


class gc_generation(ctypes.Structure):
    """
    PyGC_Head head;
    int threshold;
    int count;
    """

    _fields_ = [
        ('head'      , PyGC_Head    ),
        # collection threshold
        ('threshold' , ctypes.c_int ),
        # count of allocations or collections of younger generations
        ('count'     , ctypes.c_int ),
    ]


gc_generation_p = ctypes.POINTER(gc_generation)


###


class gc_generation_stats(ctypes.Structure):
    """
    Py_ssize_t collections;
    Py_ssize_t collected;
    Py_ssize_t uncollectable;
    """

    # Running stats per generation

    _fields_ = [
        # total number of collections
        ('collections'   , ctypes.py_ssize_t ),
        # total number of collected objects
        ('collected'     , ctypes.py_ssize_t ),
        # total number of uncollectable objects (put into gc.garbage)
        ('uncollectable' , ctypes.py_ssize_t ),
    ]


gc_generation_stats_p = ctypes.POINTER(gc_generation_stats)


### GC runtime state


NUM_GENERATIONS = 3


class _gc_runtime_state(ctypes.Structure):
    """
    PyObject *trash_delete_later;
    int trash_delete_nesting;
    int enabled;
    int debug;
    struct gc_generation generations[NUM_GENERATIONS];
    PyGC_Head *generation0;
    struct gc_generation permanent_generation;
    struct gc_generation_stats generation_stats[NUM_GENERATIONS];
    int collecting;
    PyObject *garbage;
    PyObject *callbacks;
    Py_ssize_t long_lived_total;
    Py_ssize_t long_lived_total;
    """

    _fields_ = [
        # List of objects that still need to be cleaned up, singly linked
        # via their gc headers' gc_prev pointers.
        ('trash_delete_later'   , ctypes.py_object         ),
        # Current call-stack depth of tp_dealloc calls.
        ('trash_delete_nesting' , ctypes.c_int             ),

        ('enabled'              , ctypes.c_int             ),
        ('debug'                , ctypes.c_int             ),

        # linked lists of container objects
        ('generations'          , ctypes.ARRAY(
                                      gc_generation,
                                      NUM_GENERATIONS)     ),
        ('generation0'          , PyGC_Head_p              ),

        # a permanent generation which won't be collected
        ('permanent_generation' , gc_generation            ),
        ('generation_stats'     , ctypes.ARRAY(
                                      gc_generation_stats,
                                      NUM_GENERATIONS)     ),

        # true if we are currently running the collector
        ('collecting'           , ctypes.c_int             ),
        # list of uncollectable objects
        ('garbage'              , ctypes.py_object         ),
        # a list of callbacks to be invoked when collection is performed
        ('callbacks'            , ctypes.py_object         ),

        # This is the number of objects that survived the last full
        # collection. It approximates the number of long lived objects
        # tracked by the GC.
        ('long_lived_total'     , ctypes.py_ssize_t        ),

        # This is the number of objects that survived all "non-full"
        # collections, and are awaiting to undergo a full collection for
        # the first time.
        ('long_lived_pending'   , ctypes.py_ssize_t        ),
    ]


_gc_runtime_state_p = ctypes.POINTER(_gc_runtime_state)
