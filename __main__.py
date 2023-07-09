import contextlib

from .src import PyTypeObject, PyObject


@contextlib.contextmanager
def easytest(test):
    try:
        exec(test)
        raise RuntimeWarning('patch unnecessary')
    except TypeError:
        yield
        exec(test)


###


with easytest('''
class sub_ellipsis(ellipsis := type(...)): pass
assert sub_ellipsis.mro() == [sub_ellipsis, ellipsis, object]
'''):
    tp = PyTypeObject.from_address(id(type(...)))
    tp.tp_flags |= TPFLAG('BASETYPE')


###


with easytest('''
ns = types.SimpleNamespace()
setattr(ns, 'foo', 0x_BEEF)
ns['bar'] = (0x_DEAD << 16)
assert (ns.foo ^ ns['bar']) == 0x_DEAD_BEEF
'''):
    tp = PyTypeObject.from_address(id(types.SimpleNamespace))
    tp.tp_as_mapping.contents = PyMappingMethods(
        mp_subscript = tp.tp_getattro,
        mp_ass_subscript = tp.tp_setattro,
        )
