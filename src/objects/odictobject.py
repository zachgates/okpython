__all__ = [
    '_ODictNode', '_ODictNode_p',
    '_odictobject', '_odictobject_p',
    'odictiterobject', 'odictiterobject_p',
]


import ctypes


###


class _ODictNode(ctypes.Structure): # odict keys (a simple doubly-linked list)
    """
    PyObject *key;
    Py_hash_t hash;
    _ODictNode *next;
    _ODictNode *prev;
    """


_ODictNode_p = ctypes.POINTER(_ODictNode)
_ODictNode._fields_ = [
    ('key'  , ctypes.py_object ),
    ('hash' , ctypes.py_hash_t ),
    ('next' , _ODictNode_p     ),
    ('prev' , _ODictNode_p     ),
]


###


from ..include.cpython.dictobject import PyDictObject


class _odictobject(ctypes.Structure):
    """
    PyDictObject od_dict;
    _ODictNode *od_first;
    _ODictNode *od_last;
    _ODictNode **od_fast_nodes;
    Py_ssize_t od_fast_nodes_size;
    void *od_resize_sentinel;
    size_t od_state;
    PyObject *od_inst_dict;
    PyObject *od_weakreflist;
    """

    _fields_ = [
        # the underlying dict
        ('od_dict'            , PyDictObject                 ),
        # first node in the linked list, if any
        ('od_first'           , _ODictNode_p                 ),
        # last node in the linked list, if any
        ('od_last'            , _ODictNode_p                 ),
        # hash table that mirrors the dict table
        ('od_fast_nodes'      , ctypes.POINTER(_ODictNode_p) ),
        ('od_fast_nodes_size' , ctypes.py_ssize_t            ),
        # changes if odict should be resized
        ('od_resize_sentinel' , ctypes.c_void_p              ),
        # incremented whenever the LL changes
        ('od_state'           , ctypes.c_size_t              ),
        # OrderedDict().__dict__
        ('od_inst_dict'       , ctypes.py_object             ),
        # holds weakrefs to the odict
        ('od_weakreflist'     , ctypes.py_object             ),
    ]


_odictobject_p = ctypes.POINTER(_odictobject)


###


from ..include.object import PyObject_HEAD
from ..include.odictobject import PyODictObject_p


class odictiterobject(ctypes.Structure):
    """
    PyObject_HEAD
    int kind;
    PyODictObject *di_odict;
    Py_ssize_t di_size;
    size_t di_state;
    PyObject *di_current;
    PyObject *di_result;
    """

    # The OrderedDict views (keys/values/items)

    _fields_ = [
        *PyObject_HEAD,
        ('kind'       , ctypes.c_int      ),
        ('di_odict'   , PyODictObject_p   ),
        ('di_size'    , ctypes.py_ssize_t ),
        ('di_state'   , ctypes.c_size_t   ),
        ('di_current' , ctypes.py_object  ),
        # reusable result tuple for iteritems
        ('di_result'   , ctypes.py_object ),
    ]


odictiterobject_p = ctypes.POINTER(odictiterobject)
