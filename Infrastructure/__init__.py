from .Fast_Tools import *
from .Performance_Testers import performance_compare, performance_test

import numpy as np

dummy_array_2d = np.random.rand(1000, 10).astype(np.float32)

bfill(dummy_array_2d)

del dummy_array_2d