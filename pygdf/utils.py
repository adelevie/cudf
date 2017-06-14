from collections import namedtuple

import numpy as np

from numba import njit

mask_dtype = np.dtype(np.uint8)
mask_bitsize = mask_dtype.itemsize * 8


def calc_chunk_size(size, chunksize):
    return (size + chunksize - 1) // chunksize


_TypeMinMax = namedtuple('_TypeMinMax', 'min,max')


def get_numeric_type_info(dtype):
    if dtype.kind in 'iu':
        info = np.iinfo(dtype)
        return _TypeMinMax(info.min, info.max)
    elif dtype.kind in 'f':
        return _TypeMinMax(dtype.type('-inf'), dtype.type('+inf'))
    else:
        raise TypeError(dtype)


@njit
def mask_get(mask, pos):
    return (mask[pos // mask_bitsize] >> (pos % mask_bitsize)) & 1


@njit
def mask_set(mask, pos):
    mask[pos // mask_bitsize] |= 1 << (pos % mask_bitsize)


def boolmask_to_bitmask(bools):
    masksize = calc_chunk_size(bools.size, mask_bitsize)
    mask = np.empty(masksize, dtype=mask_dtype)
    for i, x in enumerate(bools):
        if x:
            mask_set(mask, i)
    return mask
