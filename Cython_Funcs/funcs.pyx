import numpy as np
cimport numpy as np

def fill_signals_array(
    np.ndarray[np.float32_t, ndim=2] signals_array,
    list[np.ndarray] results,
    int total_assets_count,
    int start_index
) -> int:
    cdef int i
    cdef int col_end
    cdef np.ndarray[np.float32_t, ndim=2] result  # Référence temporaire pour un élément de results
    
    for i in range(len(results)):
        result = results[i]
        col_end = start_index + total_assets_count
        signals_array[:, start_index:col_end] = result
        start_index = col_end
    
    return start_index
