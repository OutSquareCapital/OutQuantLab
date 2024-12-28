import numpy as np
from Utilitary import ArrayFloat, Float32
import numbagg as nb

def bfill(array: ArrayFloat) -> ArrayFloat:
    return nb.bfill(array, axis=0) # type: ignore
    
def shift_array(returns_array: ArrayFloat, step:int = 1) -> ArrayFloat:
    shifted_array = np.empty_like(returns_array, dtype=Float32)
    shifted_array[step:, :] = returns_array[:-step, :]
    shifted_array[:step, :] = np.nan
    return shifted_array