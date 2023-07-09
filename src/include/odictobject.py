__all__ = [
    'PyODictObject', 'PyODictObject_p',
]


import ctypes


###


from ..objects.odictobject import _odictobject


class PyODictObject(_odictobject):
    ...


PyODictObject_p = ctypes.POINTER(PyODictObject)
