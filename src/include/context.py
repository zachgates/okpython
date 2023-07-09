__all__ = [
    'PyContext', 'PyContext_p',
    'PyContextVar', 'PyContextVar_p',
    'PyContextToken', 'PyContextToken_p',
]


import ctypes


###


from .internal.pycore_context import _pycontextobject


class PyContext(_pycontextobject):
    pass


PyContext_p = ctypes.POINTER(PyContext)


###


from .internal.pycore_context import _pycontextvarobject


class PyContextVar(_pycontextvarobject):
    pass


PyContextVar_p = ctypes.POINTER(PyContextVar)


###


from .internal.pycore_context import _pycontexttokenobject


class PyContextToken(_pycontexttokenobject):
    pass


PyContextToken_p = ctypes.POINTER(PyContextToken)
