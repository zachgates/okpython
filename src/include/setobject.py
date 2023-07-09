__all__ = [
    'setentry', 'setentry_p',
    'PySet_MINSIZE', 'PySetObject', 'PySetObject_p',
]


import ctypes


###


class setentry(ctypes.Structure):
    """
    PyObject *key;
    Py_hash_t hash;
    """

    # There are three kinds of entries in the table:
    #
    # 1. Unused:  key == NULL and hash == 0
    # 2. Dummy:   key == dummy and hash == -1
    # 3. Active:  key != NULL and key != dummy and hash != -1
    #
    # The hash field of Unused slots is always zero.
    #
    # The hash field of Dummy slots are set to -1
    # meaning that dummy entries can be detected by
    # either entry->key==dummy or by entry->hash==-1.

    _fields_ = [
        ('key'  , ctypes.py_object ),
        ('hash' , ctypes.py_hash_t ), # Cached hash code of the key
    ]


setentry_p = ctypes.POINTER(setentry)


###


from .object import PyObject_HEAD, PyObject_p


PySet_MINSIZE = 8


class PySetObject(ctypes.Structure):
    """
    PyObject_HEAD
    Py_ssize_t fill;
    Py_ssize_t used;
    Py_ssize_t mask;
    setentry *table;
    Py_hash_t hash;
    Py_ssize_t finger;
    setentry smalltable[PySet_MINSIZE];
    PyObject *weakreflist;
    """

    # The SetObject data structure is shared by set and frozenset objects.
    #
    # Invariant for sets:
    #   - hash is -1
    #
    # Invariants for frozensets:
    #   - data is immutable.
    #   - hash is the hash of the frozenset or -1 if not computed yet.

    _anonymous_ = ('ob_base',)
    _fields_ = [
        *PyObject_HEAD,

        ('fill'        , ctypes.py_ssize_t ), # Number active and dummy entries
        ('used'        , ctypes.py_ssize_t ), # Number active entries

        # The table contains mask + 1 slots, and that's a power of 2.
        # We store the mask instead of the size because the mask is more
        # frequently needed.
        ('mask'        , ctypes.py_ssize_t ),

        # The table points to a fixed-size smalltable for small tables
        # or to additional malloc'ed memory for bigger tables.
        # The table pointer is never NULL which saves us from repeated
        # runtime null-tests.
        ('table'       , setentry_p        ),
        ('hash'        , ctypes.py_hash_t  ), # Only used by frozenset objects
        ('finger'      , ctypes.py_ssize_t ), # Search finger for pop()

        ('_smalltable' , setentry_p        ),
        ('weakreflist' , ctypes.py_object  ), # List of weak references
    ]

    @property
    def smalltable(self):
        address = ctypes.addressof(self._smalltable)
        arr_t = ctypes.ARRAY(setentry, PySet_MINSIZE)
        return arr_t.from_address(address)


PySetObject_p = ctypes.POINTER(PySetObject)


"""
s = set(('foo', 'bar', 'baz'))
ob = PySetObject.from_address(id(s))

for entry in ob.table[:ob.mask + 1]:
    try:
        print(entry.key, entry.hash)
    except ValueError:
        continue

for entry in ob.smalltable:
    try:
        print(entry.key, entry.hash)
    except ValueError:
        continue
"""
