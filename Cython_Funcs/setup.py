from setuptools import setup # type: ignore
from Cython.Build import cythonize  # type: ignore
import numpy as np
import os

current_dir: str = os.path.abspath(".")
module_path: str = os.path.join(current_dir, "funcs.pyx")

def compile_cython():
    setup(
        ext_modules=cythonize(
            module_path,
            compiler_directives={"language_level": "3"},  # type: ignore
        ),
        include_dirs=[np.get_include()],
        script_args=["build_ext", "--inplace"]
    )

if __name__ == "__main__":
    compile_cython()