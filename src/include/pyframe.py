__all__ = [
    'PyFrameObject', 'PyFrameObject_p',
]


import ctypes


###


from .cpython.frameobject import _frame


class PyFrameObject(_frame):
    ...


PyFrameObject_p = ctypes.POINTER(PyFrameObject)
