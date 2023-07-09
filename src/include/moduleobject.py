__all__ = [
    'PyModuleDef_Base', 'PyModuleDef_Base_p', 'PyModuleDef_HEAD_INIT',
    'Py_mod_create', 'Py_mod_exec', 'PyModuleDef_Slot', 'PyModuleDef_Slot_p',
    'PyModuleDef', 'PyModuleDef_p',
]


import ctypes


###


from .object import PyObject, PyObject_p, PyObject_HEAD, _PyObject_EXTRA_INIT


class PyModuleDef_Base(ctypes.Structure):
    """
    PyObject_HEAD
    PyObject* (*m_init)(void);
    Py_ssize_t m_index;
    PyObject* m_copy;
    """

    _anonymous_ = ('ob_base',)
    _fields_ = [
        *PyObject_HEAD,
        ('m_init'  , PyObject_p        ),
        ('m_index' , ctypes.py_ssize_t ),
        ('m_copy'  , PyObject_p        ),
    ]


PyModuleDef_Base_p = ctypes.POINTER(PyModuleDef_Base)


def PyModuleDef_HEAD_INIT():
    """
    #define PyModuleDef_HEAD_INIT { \
        PyObject_HEAD_INIT(NULL)    \
        NULL, /* m_init */          \
        0,    /* m_index */         \
        NULL, /* m_copy */          \
      }
    """
    return (
        PyObject(*_PyObject_EXTRA_INIT, 1, None),
        None, 0, None
        )


###


Py_mod_create = 1
Py_mod_exec   = 2


class PyModuleDef_Slot(ctypes.Structure):
    """
    int slot;
    void *value;
    """

    _fields_ = [
        ('slot'  , ctypes.c_int    ),
        ('value' , ctypes.c_void_p ),
    ]


PyModuleDef_Slot_p = ctypes.POINTER(PyModuleDef_Slot)


###


from .object import traverseproc, inquiry, freefunc
from .methodobject import PyMethodDef_p


class PyModuleDef(ctypes.Structure):
    """
    PyModuleDef_Base m_base;
    const char* m_name;
    const char* m_doc;
    Py_ssize_t m_size;
    PyMethodDef *m_methods;
    struct PyModuleDef_Slot* m_slots;
    traverseproc m_traverse;
    inquiry m_clear;
    freefunc m_free;
    """

    _anonymous_ = ('m_base',)
    _fields_ = [
        ('m_base'     , PyModuleDef_Base   ),
        ('m_name'     , ctypes.c_char_p    ),
        ('m_doc'      , ctypes.c_char_p    ),
        ('m_size'     , ctypes.py_ssize_t  ),
        ('m_methods'  , PyMethodDef_p      ),
        ('m_slots'    , PyModuleDef_Slot_p ),
        ('m_traverse' , traverseproc       ),
        ('m_clear'    , inquiry            ),
        ('m_free'     , freefunc           ),
    ]


PyModuleDef_p = ctypes.POINTER(PyModuleDef)
