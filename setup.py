import sys


from setuptools import setup, Extension
from Cython.Build import cythonize

pkg_name = 'cython_pelt'
VERSION = '0.1.0'

install_requires = [
    "nessaid-cli"
]

ext_modules = [
    Extension(
        "cython_pelt.pelt",
        sources=[
            "cython_pelt/pelt.pyx",
        ],
    ),
]

if __name__ == '__main__':
    if len(sys.argv) == 1:
        sys.argv.append("install")

    setup(
        name=pkg_name,
        version=VERSION,
        install_requires=install_requires,
        ext_modules=cythonize(ext_modules, language_level="3"),
    )
