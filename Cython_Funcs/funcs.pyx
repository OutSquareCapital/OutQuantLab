import numpy as np
cimport numpy as np

def fill_signals_array(
    np.ndarray[np.float32_t, ndim=2] signals_array,
    list results,
    int total_assets_count,
    int start_index
) -> int:
    cdef int col_start, col_end, i
    for i in range(len(results)):
        col_start = start_index
        col_end = start_index + total_assets_count
        signals_array[:, col_start:col_end] = results[i]
        start_index = col_end
    return start_index
