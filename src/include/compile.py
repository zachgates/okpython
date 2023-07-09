__all__ = [
    'PyCompilerFlags', 'PyCompilerFlags_p', 'PyCF',
    'PyFutureFeatures', 'PyFutureFeatures_p', 'FUTURE',
    '_PyASTOptimizeState', '_PyASTOptimizeState_p',
]


import ctypes

from .. import FlagGroup


###


class PyCompilerFlags(ctypes.Structure):
    """
    int cf_flags;
    int cf_feature_version;
    """

    _fields_ = [
        # bitmask of CO_xxx flags relevant to future
        ('cf_flags'           , ctypes.c_int ),
        # minor Python version (PyCF_ONLY_AST)
        ('cf_feature_version' , ctypes.c_int ),
    ]


PyCompilerFlags_p = ctypes.POINTER(PyCompilerFlags)


###


from .cpython.code import COFLAGS


class PyCF(FlagGroup):

    def __str__(self):
        return f'{self.__class__.__name__}_{self._name_}'

    MASK                  = (0
                             | COFLAGS.FUTURE_DIVISION
                             | COFLAGS.FUTURE_ABSOLUTE_IMPORT
                             | COFLAGS.FUTURE_WITH_STATEMENT
                             | COFLAGS.FUTURE_PRINT_FUNCTION
                             | COFLAGS.FUTURE_UNICODE_LITERALS
                             | COFLAGS.FUTURE_BARRY_AS_BDFL
                             | COFLAGS.FUTURE_GENERATOR_STOP
                             | COFLAGS.FUTURE_ANNOTATIONS
                             )
    MASK_OBSOLETE         = (0
                             | COFLAGS.NESTED
                             )

    # bpo-39562: CO_FUTURE_ and PyCF_ constants must be kept unique.
    # PyCF_ constants can use bits from 0x0100 to 0x10000.
    # CO_FUTURE_ constants use bits starting at 0x20000.

    SOURCE_IS_UTF8        = ( 1 << 8  )
    DONT_IMPLY_DEDENT     = ( 1 << 9  )
    ONLY_AST              = ( 1 << 10 )
    IGNORE_COOKIE         = ( 1 << 11 )
    TYPE_COMMENTS         = ( 1 << 12 )
    ALLOW_TOP_LEVEL_AWAIT = ( 1 << 13 )
    COMPILE_MASK          = (0
                             | ONLY_AST
                             | ALLOW_TOP_LEVEL_AWAIT
                             | TYPE_COMMENTS
                             | DONT_IMPLY_DEDENT
                             )


###


class PyFutureFeatures(ctypes.Structure):
    """
    int ff_features;
    int ff_lineno;
    """

    _fields_ = [
        # flags set by future statements
        ('ff_features' , ctypes.c_int ),
        # line number of last future statement
        ('ff_lineno'   , ctypes.c_int ),
    ]


PyFutureFeatures_p = ctypes.POINTER(PyFutureFeatures)


###


class FUTURE(FlagGroup):

    def __str__(self):
        return f'{self.__class__.__name__}_{self._name_}'

    NESTED_SCOPES    = 'nested_scopes'
    GENERATORS       = 'generators'
    DIVISION         = 'division'
    ABSOLUTE_IMPORT  = 'absolute_import'
    WITH_STATEMENT   = 'with_statement'
    PRINT_FUNCTION   = 'print_function'
    UNICODE_LITERALS = 'unicode_literals'
    BARRY_AS_BDFL    = 'barry_as_FLUFL'
    GENERATOR_STOP   = 'generator_stop'
    ANNOTATIONS      = 'annotations'


###


class _PyASTOptimizeState(ctypes.Structure):
    """
    int optimize;
    int ff_features;
    """

    _fields_ = [
        ('optimize'    , ctypes.c_int ),
        ('ff_features' , ctypes.c_int ),
    ]


_PyASTOptimizeState_p = ctypes.POINTER(_PyASTOptimizeState)
