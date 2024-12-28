import os
from typing import Final

N_THREADS: Final = os.cpu_count() or 8
