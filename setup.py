import numpy as np
import os
import shutil as sh
import subprocess
import sys

from Cython.Build import cythonize
from glob import glob
from setuptools import setup, find_packages, Extension
from setuptools.command.build_ext import build_ext

# define main directories
current_dir = os.getcwd()
nomad_dir = os.path.join('nomad_sources')
nomad_build_dir = os.path.join(nomad_dir, 'build')

# Interface files
include_dirs = [
    os.path.join(nomad_dir, 'src'), # nomad headers
    os.path.join(nomad_dir, 'ext', 'sgtelib', 'src'), # sgtelib headers
    np.get_include() # numpy headers
]

source_files = glob(os.path.join('src', '*.cpp'))

# external librairies
lib_names = ['libnomad.a', 'libsgtelib.a']

# add extra objects: the librairies

# copy cpp sources code for generation
nomad_codegen_sources_dir = os.path.join('src', 'codegen', 'sources')
if os.path.exists(nomad_codegen_sources_dir):
    sh.rmtree(nomad_codegen_sources_dir)
os.makedirs(nomad_codegen_sources_dir)

# cpp files
cppfiles = [os.path.join(nomad_dir, 'src', f) for f in os.listdir(os.path.join(nomad_dir, 'src')) if f.endswith('.cpp')]
sgtelib_cppfiles = [os.path.join(nomad_dir, 'ext', 'sgtelib', 'src', f)
                    for f in os.listdir(os.path.join(nomad_dir, 'ext', 'sgtelib', 'src')) if f.endswith('.cpp')]

nomad_codegen_sources_cpp_dir = os.path.join(nomad_codegen_sources_dir, 'src')
if os.path.exists(nomad_codegen_sources_cpp_dir):  # Create destination directory
    sh.rmtree(nomad_codegen_sources_cpp_dir)
os.makedirs(nomad_codegen_sources_cpp_dir)
for f in cppfiles:  # Copy cpp files
    sh.copy(f, nomad_codegen_sources_cpp_dir)

# create external folder for sgtelib sources
if os.path.exists(os.path.join(nomad_codegen_sources_dir, 'ext')):
    sh.rmtree(os.path.join(nomad_codegen_sources_dir, 'ext'))
os.makedirs(os.path.join(nomad_codegen_sources_dir, 'ext'))

if os.path.exists(os.path.join(nomad_codegen_sources_dir, 'ext', 'sgtelib')):
    sh.rmtree(os.path.join(nomad_codegen_sources_dir, 'ext', 'sgtelib'))
os.makedirs(os.path.join(nomad_codegen_sources_dir, 'ext', 'sgtelib'))

if os.path.exists(os.path.join(nomad_codegen_sources_dir, 'ext', 'sgtelib', 'src')):
    sh.rmtree(os.path.join(nomad_codegen_sources_dir, 'ext', 'sgtelib', 'src'))
os.makedirs(os.path.join(nomad_codegen_sources_dir, 'ext', 'sgtelib', 'src'))

sgtelib_codegen_sources_cpp_dir = os.path.join(nomad_codegen_sources_dir, 'ext', 'sgtelib', 'src')
if os.path.exists(os.path.join(sgtelib_codegen_sources_cpp_dir)):
    sh.rmtree(os.path.join(sgtelib_codegen_sources_cpp_dir))
os.makedirs(os.path.join(sgtelib_codegen_sources_cpp_dir))
for f in sgtelib_cppfiles:
    sh.copy(f, sgtelib_codegen_sources_cpp_dir)

# header files
hfiles = [os.path.join(nomad_dir, 'src', f) for f in os.listdir(os.path.join(nomad_dir, 'src')) if f.endswith('.hpp')]
sgtelib_hfiles = [os.path.join(nomad_dir, 'ext', 'sgtelib', 'src', f)
                    for f in os.listdir(os.path.join(nomad_dir, 'ext', 'sgtelib', 'src')) if f.endswith('.hpp')]

for f in hfiles:
    sh.copy(f, nomad_codegen_sources_cpp_dir)
for f in sgtelib_hfiles:
    sh.copy(f, sgtelib_codegen_sources_cpp_dir)

# copy cmake files
# Nomad cmake
sh.copy(os.path.join(nomad_dir, 'CMakeLists.txt'), nomad_codegen_sources_dir)

# Sgtelib cmake
sh.copy(os.path.join(nomad_dir, 'ext', 'CMakeLists.txt'), os.path.join(nomad_codegen_sources_dir, 'ext'))
sh.copy(os.path.join(nomad_dir, 'ext', 'sgtelib', 'CMakeLists.txt'), os.path.join(nomad_codegen_sources_dir, 'ext', 'sgtelib'))

class build_ext_nomad(build_ext):

    def build_extensions(self):
        # compile nomad using Cmake

        # Create build directory
        if os.path.exists(nomad_build_dir):
            sh.rmtree(nomad_build_dir)
        os.makedirs(nomad_build_dir)
        os.chdir(nomad_build_dir)

        try:
            subprocess.check_output(['cmake', '--version'])
        except OSError:
            raise RuntimeError("CMake must be installed to build Nomad")

        # Compile static library with CMake
        subprocess.call(['cmake'] + ['..'])
        subprocess.call(['cmake', '--build', '.'])

        # Change directory back to the python interface
        os.chdir(current_dir)

        # Copy static library to src folder
        lib_nomad = [nomad_build_dir] + [lib_names[0]]
        lib_nomad = os.path.join(*lib_nomad)
        sh.copyfile(lib_nomad, os.path.join('src', lib_names[0]))

        # Copy sgtelib to src folder
        lib_sgtelib = [nomad_build_dir] + ['ext', 'sgtelib'] + [lib_names[1]]
        lib_sgtelib = os.path.join(*lib_sgtelib)
        sh.copyfile(lib_sgtelib, os.path.join('src', lib_names[1]))

        # Run extension
        build_ext.build_extensions(self)


#  _nomad = Extension('PyNomad',
#                     define_macros=[],
#                     language='c++',
#                     libraries=['nomad'],
#                     library_dirs=[os.path.join(nomad_codegen_sources_dir, 'bin')],
#                     include_dirs=[os.path.join(nomad_codegen_sources_dir, 'src'),
#                                   os.path.join(nomad_codegen_sources_dir, 'ext', 'sgtelib', 'src'),
#                                   np.get_include()],
#                     extra_objects=[os.path.join(current_dir, 'src')],
#                     sources=[os.path.join(current_dir, 'src', 'PyNomad.pyx')] + source_files,
#                     extra_compile_args=['-w'])

setup(name='PyNomad',
      version='0.0.1',
      description='A Cython wrapper to the Nomad optimization software',
      package_dir = {'PyNomad' : 'src'},
      setup_requires=['numpy', 'cython', 'setuptools'],
      packages=['PyNomad'],
      cmdclass={'build_ext': build_ext_nomad},
      ext_modules=cythonize(Extension(
          "PyNomad",
          language='c++',
          sources=[os.path.join(current_dir, 'src', 'PyNomad.pyx'),
                   os.path.join(current_dir, 'src', 'nomadCySimpleInterface.cpp')],
          include_dirs=include_dirs,
          library_dirs=[],
          extra_objects=[os.path.join('src', lib_names[0]),
                         os.path.join('src', lib_names[1])])))
