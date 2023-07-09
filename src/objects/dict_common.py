__all__ = [
    'PyDictKeyEntry', 'PyDictKeyEntry_p',
    '_dictkeysobject', '_dictkeysobject_p',
    'dict_lookup_func',
    'DKIX_EMPTY', 'DKIX_DUMMY', 'DKIX_ERROR',
]


import ctypes


###


class PyDictKeyEntry(ctypes.Structure):
    """
    Py_hash_t me_hash;
    PyObject *me_key;
    PyObject *me_value;
    """

    _fields_ = [
        # Cached hash code of me_key.
        ('me_hash'  , ctypes.py_hash_t ),
        ('me_key'   , ctypes.py_object ),
        # This field is only meaningful for combined tables
        ('me_value' , ctypes.py_object ),
    ]


PyDictKeyEntry_p = ctypes.POINTER(PyDictKeyEntry)


###


class _dictkeysobject(ctypes.Structure):
    """
    Py_ssize_t dk_refcnt;
    Py_ssize_t dk_size;
    dict_lookup_func dk_lookup;
    Py_ssize_t dk_usable;
    Py_ssize_t dk_nentries;
    char dk_indices[];
    """


_dictkeysobject_p = ctypes.POINTER(_dictkeysobject)


###


from ..include.cpython.dictobject import PyDictObject_p


# dict_lookup_func() returns index of entry
# which can be used like DK_ENTRIES(dk)[index].
# -1 when no entry found, -3 when compare raises error.
dict_lookup_func = ctypes.CFUNCTYPE(
    ctypes.py_ssize_t,
    PyDictObject_p, ctypes.py_object, ctypes.py_hash_t, ctypes.py_object_p,
)


###


DKIX_EMPTY = -1
DKIX_DUMMY = -2 # Used internally
DKIX_ERROR = -3


###


_dictkeysobject._fields_ = [
    ('dk_refcnt'   , ctypes.py_ssize_t             ),
    # Size of the hash table (dk_indices). It must be a power of 2.
    ('dk_size'     , ctypes.py_ssize_t             ),
    # Function to lookup in the hash table (dk_indices)
    ('dk_lookup'   , dict_lookup_func              ),
    # Number of usable entries in dk_entries.
    ('dk_usable'   , ctypes.py_ssize_t             ),
    # Number of used entries in dk_entries.
    ('dk_nentries' , ctypes.py_ssize_t             ),
    # char is required to avoid strict aliasing.
    ('0dk_indices' , ctypes.POINTER(ctypes.c_char) ),
]


###


from ..include.cpython.dictobject import PyDictKeysObject


PyDictKeysObject._anonymous_ = ('_',)
PyDictKeysObject._fields_ = [
    ('_' , _dictkeysobject ),
]
