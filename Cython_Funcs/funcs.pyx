import numpy as np
cimport numpy as np

cpdef int fill_signals_array(
    np.ndarray[np.float32_t, ndim=2] signals_array,
    list[np.ndarray] results,
    int total_assets_count,
    int start_index
):
    cdef int i
    cdef int end_index
    cdef np.ndarray[np.float32_t, ndim=2] result
    cdef int results_len = len(results)

    for i in range(results_len):
        result = <np.ndarray[np.float32_t, ndim=2]>results[i]
        end_index = start_index + total_assets_count
        signals_array[:, start_index:end_index] = result
        start_index = end_index
    
    return start_index