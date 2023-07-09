__all__ = [
    'PyDict_MINSIZE',
    'DK_SIZE', 'DK_IXSIZE', 'DK_ENTRIES', 'DK_MASK', 'IS_POWER_OF_2',
    'USABLE_FRACTION', 'ESTIMATE_SIZE', 'GROWTH_RATE',
    'dictiterobject', 'dictiterobject_p',
]


import ctypes

from .dict_common import PyDictKeyEntry


###


# PyDict_MINSIZE is the starting size for any new dict.
# 8 allows dicts with no more than 5 active entries; experiments suggested
# this suffices for the majority of dicts (consisting mostly of usually-small
# dicts created to pass keyword arguments).
# Making this 8, rather than 4 reduces the number of resizes for most
# dictionaries, without any significant extra memory use.
PyDict_MINSIZE = 8


###


def DK_SIZE(dk) -> int:
    """
    #define DK_SIZE(dk) ((dk)->dk_size)
    """
    return dk.dk_size


if ctypes.pyconfig.SIZEOF_VOID_P > 4:

    def DK_IXSIZE(dk) -> int:
        """
        #define DK_IXSIZE(dk)                          \
            (DK_SIZE(dk) <= 0xff ?                     \
                1 : DK_SIZE(dk) <= 0xffff ?            \
                    2 : DK_SIZE(dk) <= 0xffffffff ?    \
                        4 : sizeof(int64_t))
        """
        if DK_SIZE(dk) <= 0xFF:
            return 1
        elif DK_SIZE(dk) <= 0xFFFF:
            return 2
        elif DK_SIZE(dk) <= 0xFFFFFFFF:
            return 4
        else:
            return 8

else:

    def DK_IXSIZE(dk) -> int:
        """
        #define DK_IXSIZE(dk)                          \
            (DK_SIZE(dk) <= 0xff ?                     \
                1 : DK_SIZE(dk) <= 0xffff ?            \
                    2 : sizeof(int32_t))
        """
        if DK_SIZE(dk) <= 0xFF:
            return 1
        elif DK_SIZE(dk) <= 0xFFFF:
            return 2
        else:
            return 4


def DK_ENTRIES(dk):
    """
    #define DK_ENTRIES(dk) \
        ((PyDictKeyEntry*)(&((int8_t*)((dk)->dk_indices))[DK_SIZE(dk) * DK_IXSIZE(dk)]))
    """
    return ctypes.ARRAY(PyDictKeyEntry, dk.dk_nentries).from_address(
        ctypes.addressof(dk.dk_indices) + (DK_SIZE(dk) * DK_IXSIZE(dk))
        )


def DK_MASK(dk) -> int:
    """
    #define DK_MASK(dk) (((dk)->dk_size)-1)
    """
    return (dk.dk_size - 1)


def IS_POWER_OF_2(x: int) -> bool:
    """
    #define IS_POWER_OF_2(x) (((x) & (x-1)) == 0)
    """
    return ((x & (x - 1)) == 0)


###


# USABLE_FRACTION is the maximum dictionary load.
# Increasing this ratio makes dictionaries more dense resulting in more
# collisions.  Decreasing it improves sparseness at the expense of spreading
# indices over more cache lines and at the cost of total memory consumed.
# - USABLE_FRACTION must obey the following:
#   (0 < USABLE_FRACTION(n) < n) for all n >= 2
# - USABLE_FRACTION should be quick to calculate.
# - Fractions around 1/2 to 2/3 seem to work well in practice.
def USABLE_FRACTION(n: int) -> float:
    """
    #define USABLE_FRACTION(n) (((n) << 1)/3)
    """
    return ((n << 1) / 3)


# ESTIMATE_SIZE is reverse function of USABLE_FRACTION.
# This can be used to reserve enough size to insert n entries without
# resizing.
def ESTIMATE_SIZE(n: int) -> int:
    """
    #define ESTIMATE_SIZE(n)  (((n)*3+1) >> 1)
    """
    return ((n * 3 + 1) >> 1)


# GROWTH_RATE. Growth rate upon hitting maximum load.
# Currently set to used*3.
# This means that dicts double in size when growing without deletions,
# but have more head room when the number of deletions is on a par with the
# number of insertions.  See also bpo-17563 and bpo-33205.
def GROWTH_RATE(d) -> int:
    """
    #define GROWTH_RATE(d) ((d)->ma_used*3)
    """
    return (d.ma_used * 3)


###


from ..include.object import PyObject_HEAD
from ..include.cpython.dictobject import PyDictObject_p


class dictiterobject(ctypes.Structure):
    """
    PyObject_HEAD
    PyDictObject *di_dict;
    Py_ssize_t di_used;
    Py_ssize_t di_pos;
    PyObject* di_result;
    Py_ssize_t len;
    """

    _anonymous_ = ('ob_base',)
    _fields_ = [
        *PyObject_HEAD,
        # Set to NULL when iterator is exhausted
        ('di_dict'   , PyDictObject_p    ),
        ('di_used'   , ctypes.py_ssize_t ),
        ('di_pos'    , ctypes.py_ssize_t ),
        # reusable result tuple for iteritems
        ('di_result' , ctypes.py_object  ),
        ('len'       , ctypes.py_ssize_t ),
    ]


dictiterobject_p = ctypes.POINTER(dictiterobject)
