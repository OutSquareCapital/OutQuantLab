from numbagg import bfill

from numquant.arrays.create import create_empty_like
from numquant.main import Float2D, Int2D, Nan, np


def reduce(array: Float2D, frequency: int) -> Float2D:
    array_length: int = array.shape[0]
    indices: Int2D = np.arange(start=0, stop=array_length, step=frequency)

    if array_length % frequency != 0:
        selected_indices: Int2D = np.append(arr=indices, values=array_length - 1)
        return array[selected_indices]
    return array[indices]


def shift(original: Float2D, step: int = 1) -> Float2D:
    shifted: Float2D = create_empty_like(model=original)
    shifted[step:, :] = original[:-step, :]
    shifted[:step, :] = Nan
    return shifted

def backfill(array: Float2D) -> Float2D:
    return bfill(array, axis=0)  # type: ignore


def fill_nan(array: Float2D) -> Float2D:
    result: Float2D = array.copy()
    mask = np.isnan(array)
    idx = np.arange(array.shape[0])[:, None]
    valid_mask = ~mask
    first_valid_idx = np.min(np.where(valid_mask, idx, array.shape[0]), axis=0)
    cond = (idx > first_valid_idx) & mask
    result[cond] = 0
    return result

def fill_nan_with_data(base_array: Float2D, array_filler: Float2D) -> Float2D:
    return np.where(np.isnan(base_array), array_filler, base_array)