import numpy as np
import numbagg as nb

def bfill(array: np.ndarray) -> np.ndarray:
    return nb.bfill(array, axis=0)
    
def shift_array(returns_array: np.ndarray, step:int = 1) -> np.ndarray:
    shifted_array = np.empty_like(returns_array, dtype=np.float32)
    shifted_array[step:, :] = returns_array[:-step, :]
    shifted_array[:step, :] = np.nan
    return shifted_array
