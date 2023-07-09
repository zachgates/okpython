__all__ = [
    'PyHamtNode', 'PyHamtNode_p',
    'PyHamtObject', 'PyHamtObject_p',
    'PyHamtIteratorState', 'PyHamtIteratorState_p',
    'PyHamtIterator', 'PyHamtIterator_p',
]


import ctypes

from ..object import PyObject_HEAD


###


class PyHamtNode(ctypes.Structure):
    """
    PyObject_HEAD
    """

    # Abstract tree node.

    _fields_ = [
        *PyObject_HEAD,
    ]


PyHamtNode_p = ctypes.POINTER(PyHamtNode)


###


class PyHamtObject(ctypes.Structure):
    """
    PyObject_HEAD
    PyHamtNode *h_root;
    PyObject *h_weakreflist;
    Py_ssize_t h_count;
    """

    # An HAMT immutable mapping collection.

    _fields_ = [
        *PyObject_HEAD,
        ('h_root'        , PyHamtNode_p      ),
        ('h_weakreflist' , ctypes.py_object  ),
        ('h_count'       , ctypes.py_ssize_t ),
    ]


PyHamtObject_p = ctypes.POINTER(PyHamtObject)


###


class PyHamtIteratorState(ctypes.Structure):
    """
    PyHamtNode *i_nodes[_Py_HAMT_MAX_TREE_DEPTH];
    Py_ssize_t i_pos[_Py_HAMT_MAX_TREE_DEPTH];
    int8_t i_level;
    """

    # A struct to hold the state of depth-first traverse of the tree.
    #
    # HAMT is an immutable collection.  Iterators will hold a strong reference
    # to it, and every node in the HAMT has strong references to its children.
    #
    # So for iterators, we can implement zero allocations and zero reference
    # inc/dec depth-first iteration.
    #
    # - i_nodes: an array of seven pointers to tree nodes
    # - i_level: the current node in i_nodes
    # - i_pos: an array of positions within nodes in i_nodes.

    _fields_ = [
        ('i_nodes' , PyHamtNode_p      ),
        ('i_pos'   , ctypes.py_ssize_t ),
        ('i_level' , ctypes.c_int8     ),
    ]


PyHamtIteratorState_p = ctypes.POINTER(PyHamtIteratorState)


###


from ..object import binaryfunc


class PyHamtIterator(ctypes.Structure):
    """
    PyObject_HEAD
    PyHamtObject *hi_obj;
    PyHamtIteratorState hi_iter;
    binaryfunc hi_yield;
    """

    # Base iterator object.
    #
    # Contains the iteration state, a pointer to the HAMT tree,
    # and a pointer to the 'yield function'.  The latter is a simple
    # function that returns a key/value tuple for the 'Items' iterator,
    # just a key for the 'Keys' iterator, and a value for the 'Values'
    # iterator.

    _fields_ = [
        *PyObject_HEAD,
        ('hi_obj'   , PyHamtObject_p      ),
        ('hi_iter'  , PyHamtIteratorState ),
        ('hi_yield' , binaryfunc          ),
    ]


PyHamtIterator_p = ctypes.POINTER(PyHamtIterator)
