from setuptools import setup # type: ignore
from Cython.Build import cythonize  # type: ignore
import numpy as np
import os

module_path: str = os.path.abspath("funcs.pyx")

setup(
    ext_modules=cythonize(
        module_path,
        compiler_directives={"language_level": "3"},  # type: ignore
    ),
    include_dirs=[np.get_include()],
)
