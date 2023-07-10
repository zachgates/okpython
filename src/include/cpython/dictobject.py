__all__ = [
    'PyDictKeysObject', 'PyDictKeysObject_p',
    'PyDictObject', 'PyDictObject_p',
    'PyDict_GET_SIZE', '_PyDict_HasSplitTable',
    '_PyDictViewObject', '_PyDictViewObject_p',
]


import ctypes

from ... import PyAPI_FUNC
from ..object import PyObject_HEAD, PyObject_p


###


from ...objects.dict_common import _dictkeysobject, PyDictKeyEntry


class PyDictKeysObject(ctypes.Structure): # _dictkeysobject

    @property
    def dk_indices(self):
        """
        Actual hash table of dk_size entries.
        It holds indices in dk_entries, or DKIX_EMPTY(-1) or DKIX_DUMMY(-2).

        Indices must be: 0 <= indice < USABLE_FRACTION(dk_size).

        The size in bytes of an indice depends on dk_size:

        - 1 byte if dk_size <= 0xff (char*)
        - 2 bytes if dk_size <= 0xffff (int16_t*)
        - 4 bytes if dk_size <= 0xffffffff (int32_t*)
        - 8 bytes otherwise (int64_t*)

        Dynamically sized, SIZEOF_VOID_P is minimum.
        """

        if self.dk_size <= 0xFF:
            typ = ctypes.c_int8
        elif self.dk_size <= 0xFFFF:
            typ = ctypes.c_int16
        elif self.dk_size <= 0xFFFFFFFF:
            typ = ctypes.c_int32
        else:
            typ = ctypes.c_int64

        address = ctypes.addressof(getattr(self, '0dk_indices'))
        size = max(ctypes.pyconfig.SIZEOF_VOID_P, self.dk_size)
        return ctypes.ARRAY(typ, size).from_address(address)


PyDictKeysObject_p = ctypes.POINTER(PyDictKeysObject)


###


class PyDictObject(ctypes.Structure):
    """
    PyObject_HEAD
    Py_ssize_t ma_used;
    uint64_t ma_version_tag;
    PyDictKeysObject *ma_keys;
    PyObject **ma_values;
    """

    # The ma_values pointer is NULL for a combined table
    # or points to an array of PyObject* for a split table
    # - If ma_values is NULL, the table is "combined": keys and values
    #   are stored in ma_keys.
    # - If ma_values is not NULL, the table is splitted:
    #   keys are stored in ma_keys and values are stored in ma_values

    _anonymous_ = ('ob_base',)
    _fields_ = [
        *PyObject_HEAD,

        # Number of items in the dictionary
        ('ma_used'        , ctypes.py_ssize_t  ),

        # Dictionary version: globally unique, value change each time
        # the dictionary is modified
        ('ma_version_tag' , ctypes.c_uint64    ),

        ('ma_keys'        , PyDictKeysObject_p ),
        ('ma_values'      , ctypes.py_object_p ),
    ]


PyDictObject_p = ctypes.POINTER(PyDictObject)


###


from ..object import PyObject_pp
from .object import _Py_Identifier_p


PyAPI_FUNC("_PyDict_GetItem_KnownHash",
    restype = PyObject_p,
    argtypes = [
        PyObject_p,       # mp
        PyObject_p,       # key
        ctypes.py_hash_t, # hash
    ])

PyAPI_FUNC("_PyDict_GetItemIdWithError",
    restype = PyObject_p,
    argtypes = [
        PyObject_p,       # dp
        _Py_Identifier_p, # key
    ])

PyAPI_FUNC("_PyDict_GetItemStringWithError",
    restype = PyObject_p,
    argtypes = [
        PyObject_p,
        ctypes.c_char_p,
    ])

PyAPI_FUNC("PyDict_SetDefault",
    restype = PyObject_p,
    argtypes = [
        PyObject_p, # mp
        PyObject_p, # key
        PyObject_p, # defaultobj
    ])

PyAPI_FUNC("_PyDict_SetItem_KnownHash",
    restype = ctypes.c_int,
    argtypes = [
        PyObject_p,       # mp
        PyObject_p,       # key
        PyObject_p,       # item
        ctypes.py_hash_t, # hash
    ])

PyAPI_FUNC("_PyDict_DelItem_KnownHash",
    restype = ctypes.c_int,
    argtypes = [
        PyObject_p,       # mp
        PyObject_p,       # key
        ctypes.py_hash_t, # hash
    ])

PyAPI_FUNC("_PyDict_DelItemIf",
    restype = ctypes.c_int,
    argtypes = [
        PyObject_p,       # mp
        PyObject_p,       # key
        ctypes.CFUNCTYPE( # predicate
            ctypes.c_int,
            PyObject_p,   # value
            ),
    ])

PyAPI_FUNC("PyObject_GenericGetDict",
    restype = PyObject_p,
    argtypes = [
        PyObject_p,
        ctypes.c_void_p,
    ])

PyAPI_FUNC("_PyDict_Next",
    restype = ctypes.c_int,
    argtypes = [
        PyObject_p,        # mp
        ctypes.py_ssize_t, # pos
        PyObject_pp,       # key
        PyObject_pp,       # value
        ctypes.py_hash_t,  # hash
    ])


###


def PyDict_GET_SIZE(mp):
    """
    #define PyDict_GET_SIZE(mp)  (assert(PyDict_Check(mp)),((PyDictObject *)mp)->ma_used)
    """
    assert ctypes.abi.PyDict_Check(mp)
    mp = ctypes.cast(ctypes.byref(mp), PyDictObject_p)
    return mp.contents.ma_used


###


PyAPI_FUNC("_PyDict_Contains",
    restype = ctypes.c_int,
    argtypes = [
        PyObject_p,       # mp
        PyObject_p,       # key
        ctypes.py_hash_t, # hash
    ])

PyAPI_FUNC("_PyDict_NewPresized",
    restype = PyObject_p,
    argtypes = [
        ctypes.py_ssize_t, # minused
    ])

PyAPI_FUNC("_PyDict_MaybeUntrack",
    argtypes = [
        PyObject_p, # mp
    ])

PyAPI_FUNC("_PyDict_HasOnlyStringKeys",
    restype = ctypes.c_int,
    argtypes = [
        PyObject_p, # mp
    ])

PyAPI_FUNC("_PyDict_SizeOf",
    restype = ctypes.py_ssize_t,
    argtypes = [
        PyDictObject_p,
    ])

PyAPI_FUNC("_PyDict_Pop",
    restype = PyObject_p,
    argtypes = [
        PyObject_p,
        PyObject_p,
        PyObject_p,
    ])


###


def _PyDict_HasSplitTable(d):
    """
    #define _PyDict_HasSplitTable(d) ((d)->ma_values != NULL)
    """
    return bool(d.ma_values)


###


# Like PyDict_Merge, but override can be 0, 1 or 2.  If override is 0,
# the first occurrence of a key wins, if override is 1, the last occurrence
# of a key wins, if override is 2, a KeyError with conflicting key as
# argument is raised.
PyAPI_FUNC("_PyDict_MergeEx",
    restype = ctypes.c_int,
    argtypes = [
        PyObject_p,   # mp
        PyObject_p,   # other
        ctypes.c_int, # override
    ])

PyAPI_FUNC("_PyDict_GetItemId",
    restype = PyObject_p,
    argtypes = [
        PyObject_p,       # dp
        _Py_Identifier_p, # key
    ])

PyAPI_FUNC("_PyDict_SetItemId",
    restype = ctypes.c_int,
    argtypes = [
        PyObject_p,       # dp
        _Py_Identifier_p, # key
        PyObject_p,       # item
    ])

PyAPI_FUNC("_PyDict_DelItemId",
    restype = ctypes.c_int,
    argtypes = [
        PyObject_p,       # mp
        _Py_Identifier_p, # key
    ])

PyAPI_FUNC("_PyDict_DebugMallocStats",
    argtypes = [
        ctypes.c_void_p, # FILE *out
    ])


###


class _PyDictViewObject(ctypes.Structure):
    """
    PyObject_HEAD
    PyDictObject *dv_dict;
    """

    _anonymous_ = ('ob_base',)
    _fields_ = [
        *PyObject_HEAD,
        ('dv_dict' , PyDictObject_p ),
    ]


_PyDictViewObject_p = ctypes.POINTER(_PyDictViewObject)


###


from ..object import PyTypeObject_p


PyAPI_FUNC("_PyDictView_New",
    restype = PyObject_p,
    argtypes = [
        PyObject_p,
        PyTypeObject_p,
    ])

PyAPI_FUNC("_PyDictView_Intersect",
    restype = PyObject_p,
    argtypes = [
        PyObject_p, # self
        PyObject_p, # other
    ])
