__all__ = [
    'PyMemberDef', 'PyMemberDef_p',
    'T',
    'READONLY', 'READ_RESTRICTED', 'PY_WRITE_RESTRICTED', 'RESTRICTED',
]


import ctypes


###


class PyMemberDef(ctypes.Structure):
    """
    const char *name;
    int type;
    Py_ssize_t offset;
    int flags;
    const char *doc;
    """

    _fields_ = [
        ('name'   , ctypes.c_char_p   ),
        ('type'   , ctypes.c_int      ),
        ('offset' , ctypes.py_ssize_t ),
        ('flags'  , ctypes.c_int      ),
        ('doc'    , ctypes.c_char_p   ),
    ]


PyMemberDef_p = ctypes.POINTER(PyMemberDef)


###


import enum

from .. import MacroFactoryGroup


class T(enum.Enum, metaclass = MacroFactoryGroup):

    def __init__(self, variant: int, value: type, doc: str):
        if not isinstance(variant, int):
            raise TypeError('an integer is required for enum variant')

        if not isinstance(doc, str):
            raise TypeError('a string is required for enum docstring')

        if not (isinstance(value, type) and \
                issubclass(value, ctypes.Structure.__base__)):
            raise TypeError('a C type Structure is required for enum value')

        self.__doc__ = doc
        self._value_ = (variant, value)

    @property
    def variant(self):
        return self._value_[0]

    @property
    def value(self):
        return self._value_[1]

    __call__ = value

    def __str__(self):
        return f'{self.__class__.__name__}_{self._name_}'

    def __repr__(self):
        return ('<%(name)s: (variant=%(variant)i, value=ctypes.%(value)s)>'
                % {'name': self.__str__(),
                   'variant': self.variant,
                   'value': self.value.__name__})


class T(T):
    """
    Types
    """

    VOIDP          = ( -1 , ctypes.c_void_p    , 'void *'             )
    SHORT          = (  0 , ctypes.c_short     , 'short'              )
    INT            = (  1 , ctypes.c_int       , 'int'                )
    LONG           = (  2 , ctypes.c_long      , 'long'               )
    FLOAT          = (  3 , ctypes.c_float     , 'float'              )
    DOUBLE         = (  4 , ctypes.c_double    , 'double'             )
    STRING         = (  5 , ctypes.c_char_p    , 'const char *'       )
    OBJECT         = (  6 , ctypes.py_object   , 'PyObject *'         )
    CHAR           = (  7 , ctypes.c_char      , 'char'               )
    BYTE           = (  8 , ctypes.c_byte      , 'char'               )
    UBYTE          = (  9 , ctypes.c_ubyte     , 'unsigned char'      )
    USHORT         = ( 10 , ctypes.c_ushort    , 'unsigned short'     )
    UINT           = ( 11 , ctypes.c_uint      , 'unsigned int'       )
    ULONG          = ( 12 , ctypes.c_ulong     , 'unsigned long'      )
    STRING_INPLACE = ( 13 , ctypes.c_char_p    , 'const char *'       )
    BOOL           = ( 14 , ctypes.c_byte      , 'char'               )
    OBJECT_EX      = ( 16 , ctypes.py_object   , 'PyObject *'         )
    LONGLONG       = ( 17 , ctypes.c_longlong  , 'long long'          )
    ULONGLONG      = ( 18 , ctypes.c_ulonglong , 'unsigned long long' )
    PYSSIZET       = ( 19 , ctypes.py_ssize_t  , 'Py_ssize_t'         )
    NONE           = ( 20 , ctypes.py_object   , 'PyObject *'         )


# factor = pow(256, ctypes.sizeof(typ)) - 1   # base
# rng = (~(rng := factor // 2), rng)          # signed
# rng = (0, factor)                           # unsigned


###


READONLY            = 1
READ_RESTRICTED     = 2
PY_WRITE_RESTRICTED = 4
RESTRICTED          = (READ_RESTRICTED | PY_WRITE_RESTRICTED)
