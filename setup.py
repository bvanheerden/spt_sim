from distutils.core import setup
from Cython.Build import cythonize

setup(
    ext_modules=cythonize(["basic_sim.pyx"])#, "sim_module_c.pyx"])
)
