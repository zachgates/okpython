__all__ = [
    'PyDict_Check', 'PyDict_CheckExact',
    'PyDictKeys_Check', 'PyDictValues_Check', 'PyDictItems_Check',
    'PyDictViewSet_Check',
]


import ctypes

from .. import PyAPI_DATA, PyAPI_FUNC
from .object import PyTypeObject, PyObject_p, PyObject_pp


###


PyAPI_DATA("PyDict_Type",
    dtype = PyTypeObject,
    )


###


from .object import Py_TYPE, Py_IS_TYPE, PyType_FastSubclass, TPFLAG


def PyDict_Check(op):
    """
    #define PyDict_Check(op) \
                     PyType_FastSubclass(Py_TYPE(op), Py_TPFLAGS_DICT_SUBCLASS)
    """
    return PyType_FastSubclass(Py_TYPE(op), TPFLAG('DICT_SUBCLASS'))


def PyDict_CheckExact(op):
    """
    #define PyDict_CheckExact(op) Py_IS_TYPE(op, &PyDict_Type)
    """
    return Py_IS_TYPE(op, PyDict_Type)


###


PyAPI_FUNC("PyDict_New",
    restype = PyObject_p,
    )

PyAPI_FUNC("PyDict_GetItem",
    restype = PyObject_p,
    argtypes = [
        PyObject_p, # mp
        PyObject_p, # key
    ])

PyAPI_FUNC("PyDict_GetItemWithError",
    restype = PyObject_p,
    argtypes = [
        PyObject_p, # mp
        PyObject_p, # key
    ])

PyAPI_FUNC("PyDict_SetItem",
    restype = ctypes.c_int,
    argtypes = [
        PyObject_p, # mp
        PyObject_p, # key
        PyObject_p, # item
    ])

PyAPI_FUNC("PyDict_DelItem",
    restype = ctypes.c_int,
    argtypes = [
        PyObject_p, # mp
        PyObject_p, # key
    ])

PyAPI_FUNC("PyDict_Clear",
    argtypes = [
        PyObject_p, # mp
    ])

PyAPI_FUNC("PyDict_Next",
    restype = ctypes.c_int,
    argtypes = [
        PyObject_p,        # mp
        ctypes.py_ssize_t, # pos
        PyObject_pp,       # key
        PyObject_pp,       # value
    ])

PyAPI_FUNC("PyDict_Keys",
    restype = PyObject_p,
    argtypes = [
        PyObject_p, # mp
    ])

PyAPI_FUNC("PyDict_Values",
    restype = PyObject_p,
    argtypes = [
        PyObject_p, # mp
    ])

PyAPI_FUNC("PyDict_Items",
    restype = PyObject_p,
    argtypes = [
        PyObject_p, # mp
    ])

PyAPI_FUNC("PyDict_Size",
    restype = ctypes.py_ssize_t,
    argtypes = [
        PyObject_p, # mp
    ])

PyAPI_FUNC("PyDict_Copy",
    restype = PyObject_p,
    argtypes = [
        PyObject_p, # mp
    ])

PyAPI_FUNC("PyDict_Contains",
    restype = ctypes.c_int,
    argtypes = [
        PyObject_p, # mp
        PyObject_p, # key
    ])

# PyDict_Update(mp, other) is equivalent to PyDict_Merge(mp, other, 1).
PyAPI_FUNC("PyDict_Update",
    restype = ctypes.c_int,
    argtypes = [
        PyObject_p, # mp
        PyObject_p, # other
    ])

# PyDict_Merge updates/merges from a mapping object (an object that
# supports PyMapping_Keys() and PyObject_GetItem()).  If override is true,
# the last occurrence of a key wins, else the first.  The Python
# dict.update(other) is equivalent to PyDict_Merge(dict, other, 1).
PyAPI_FUNC("PyDict_Merge",
    restype = ctypes.c_int,
    argtypes = [
        PyObject_p,   # mp
        PyObject_p,   # other
        ctypes.c_int, # override
    ])

# PyDict_MergeFromSeq2 updates/merges from an iterable object producing
# iterable objects of length 2.  If override is true, the last occurrence
# of a key wins, else the first.  The Python dict constructor dict(seq2)
# is equivalent to dict={}; PyDict_MergeFromSeq(dict, seq2, 1).
PyAPI_FUNC("PyDict_MergeFromSeq2",
    restype = ctypes.c_int,
    argtypes = [
        PyObject_p,   # d
        PyObject_p,   # seq2
        ctypes.c_int, # override
    ])

PyAPI_FUNC("PyDict_GetItemString",
    restype = PyObject_p,
    argtypes = [
        PyObject_p,      # dp
        ctypes.c_char_p, # key
    ])

PyAPI_FUNC("PyDict_SetItemString",
    restype = ctypes.c_int,
    argtypes = [
        PyObject_p,      # dp
        ctypes.c_char_p, # key
        PyObject_p,      # item
    ])

PyAPI_FUNC("PyDict_DelItemString",
    restype = ctypes.c_int,
    argtypes = [
        PyObject_p,      # dp
        ctypes.c_char_p, # key
    ])


###


PyAPI_DATA("PyDictKeys_Type",
    dtype = PyTypeObject,
    )

PyAPI_DATA("PyDictValues_Type",
    dtype = PyTypeObject,
    )

PyAPI_DATA("PyDictItems_Type",
    dtype = PyTypeObject,
    )


###


from .object import PyObject_TypeCheck


def PyDictKeys_Check(op):
    """
    #define PyDictKeys_Check(op) PyObject_TypeCheck(op, &PyDictKeys_Type)
    """
    return PyObject_TypeCheck(op, PyDictKeys_Type)


def PyDictValues_Check(op):
    """
    #define PyDictValues_Check(op) PyObject_TypeCheck(op, &PyDictValues_Type)
    """
    return PyObject_TypeCheck(op, PyDictValues_Type)


def PyDictItems_Check(op):
    """
    #define PyDictItems_Check(op) PyObject_TypeCheck(op, &PyDictItems_Type)
    """
    return PyObject_TypeCheck(op, PyDictItems_Type)


# This excludes Values, since they are not sets.
def PyDictViewSet_Check(op):
    """
    # define PyDictViewSet_Check(op) \
        (PyDictKeys_Check(op) || PyDictItems_Check(op))
    """
    return (PyDictKeys_Check(op) or PyDictItems_Check(op))


### Dictionary (key, value, items) iterators


PyAPI_DATA("PyDictIterKey_Type",
    dtype = PyTypeObject,
    )

PyAPI_DATA("PyDictIterValue_Type",
    dtype = PyTypeObject,
    )

PyAPI_DATA("PyDictIterItem_Type",
    dtype = PyTypeObject,
    )

PyAPI_DATA("PyDictRevIterKey_Type",
    dtype = PyTypeObject,
    )

PyAPI_DATA("PyDictRevIterItem_Type",
    dtype = PyTypeObject,
    )

PyAPI_DATA("PyDictRevIterValue_Type",
    dtype = PyTypeObject,
    )
