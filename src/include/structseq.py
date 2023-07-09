__all__ = [
    'PyStructSequence_Field', 'PyStructSequence_Field_p',
    'PyStructSequence_Desc', 'PyStructSequence_Desc_p',
    'PyStructSequence_UnnamedField', 'PyStructSequence_UnnamedField_p',
    'PyStructSequence', 'PyStructSequence_p',
]


import ctypes


###


class PyStructSequence_Field(ctypes.Structure):
    """
    const char *name;
    const char *doc;
    """

    _fields_ = [
        ('name' , ctypes.c_char_p ),
        ('doc'  , ctypes.c_char_p ),
    ]


PyStructSequence_Field_p = ctypes.POINTER(PyStructSequence_Field)


###


class PyStructSequence_Desc(ctypes.Structure):
    """
    const char *name;
    const char *doc;
    struct PyStructSequence_Field *fields;
    int n_in_sequence;
    """

    _fields_ = [
        ('name'          , ctypes.c_char_p          ),
        ('doc'           , ctypes.c_char_p          ),
        ('fields'        , PyStructSequence_Field_p ),
        ('n_in_sequence' , ctypes.c_int             ),
    ]


PyStructSequence_Desc_p = ctypes.POINTER(PyStructSequence_Desc)


###


PyStructSequence_UnnamedField = ctypes.c_char_p
PyStructSequence_UnnamedField_p = ctypes.POINTER(PyStructSequence_UnnamedField)


###


from .cpython.tupleobject import PyTupleObject


class PyStructSequence(PyTupleObject):
    """
    typedef PyTupleObject PyStructSequence
    """


PyStructSequence_p = ctypes.POINTER(PyStructSequence)
