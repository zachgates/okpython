__all__ = [
    '_PyGenObject_HEAD', 'PyGenObject', 'PyGenObject_p',
    'PyCoroObject', 'PyCoroObject_p',
    'PyAsyncGenObject', 'PyAsyncGenObject_p',
]


import ctypes


###


from .object import PyObject_HEAD
from .pyframe import PyFrameObject_p
from .cpython.pystate import _PyErr_StackItem


def _PyGenObject_HEAD(prefix):
    """
    _PyGenObject_HEAD defines the initial segment of generator
    and coroutine objects.
    """
    return (
        *PyObject_HEAD,
        # Note: gi_frame can be NULL if the generator is "finished"
        (f'{prefix}_frame'       , PyFrameObject_p  ),
        # True if generator is being executed.
        (f'{prefix}_running'     , ctypes.c_char    ),
        # The code object backing the generator
        (f'{prefix}_code'        , ctypes.py_object ),
        # List of weak reference.
        (f'{prefix}_weakreflist' , ctypes.py_object ),
        # Name of the generator.
        (f'{prefix}_name'        , ctypes.py_object ),
        # Qualified name of the generator.
        (f'{prefix}_qualname'    , ctypes.py_object ),
        (f'{prefix}_exc_state'   , _PyErr_StackItem ),
    )


###


class PyGenObject(ctypes.Structure):
    """
    _PyGenObject_HEAD(gi)
    """

    # The gi_ prefix is intended to remind of generator-iterator.

    _anonymous_ = ('ob_base',)
    _fields_ = [
        *_PyGenObject_HEAD('gi'),
    ]


PyGenObject_p = ctypes.POINTER(PyGenObject)


###


class PyCoroObject(ctypes.Structure):
    """
    _PyGenObject_HEAD(cr)
    PyObject *cr_origin;
    """

    _anonymous_ = ('ob_base',)
    _fields_ = [
        *_PyGenObject_HEAD('cr'),
        ('cr_origin' , ctypes.py_object ),
    ]


PyCoroObject_p = ctypes.POINTER(PyCoroObject)


### Asynchronous Generators


class PyAsyncGenObject(ctypes.Structure):
    """
    _PyGenObject_HEAD(ag)
    PyObject *ag_finalizer;
    int ag_hooks_inited;
    int ag_closed;
    int ag_running_async;
    """

    _anonymous_ = ('ob_base',)
    _fields_ = [
        *_PyGenObject_HEAD('ag'),
        ('ag_finalizer'     , ctypes.py_object ),

        # Flag is set to 1 when hooks set up by sys.set_asyncgen_hooks
        # were called on the generator, to avoid calling them more
        # than once.
        ('ag_hooks_inited'  , ctypes.c_int     ),

        # Flag is set to 1 when aclose() is called for the first time, or
        # when a StopAsyncIteration exception is raised.
        ('ag_closed'        , ctypes.c_int     ),

        ('ag_running_async' , ctypes.c_int     ),
    ]


PyAsyncGenObject_p = ctypes.POINTER(PyAsyncGenObject)
