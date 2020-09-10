# ----------------------------------------------------------------------------
#  Root CMake file for Nomad
# ----------------------------------------------------------------------------

# cmake version : the latest one
cmake_minimum_required(VERSION 3.9 FATAL_ERROR)

# name of the project
project (Nomad LANGUAGES CXX)

# use standard compilers parameters for c++11
SET( CMAKE_CXX_STANDARD 11 )
SET( CMAKE_CXX_STANDARD_REQUIRED ON )

# Disable in-source builds to prevent source tree corruption.
if(" ${CMAKE_SOURCE_DIR}" STREQUAL " ${CMAKE_BINARY_DIR}")
    message(FATAL_ERROR "FATAL: In-source builds are not allowed.
    You should create a separate directory for build files.
    ")
endif()

#check compiler version
if ("${CMAKE_CXX_COMPILER_ID}" STREQUAL "GNU")
    # require at least gcc 4
    if (CMAKE_CXX_COMPILER_VERSION VERSION_LESS 4)
        message(FATAL_ERROR "GCC version < 4 has not been tested for Nomad!")
    endif()
elseif (("${CMAKE_CXX_COMPILER_ID}" MATCHES "Clang") 
    OR ("${CMAKE_CXX_COMPILER_ID}" STREQUAL "Clang"))
    # require at least clang 5
    if (CMAKE_CXX_COMPILER_VERSION VERSION_LESS 5)
        message(FATAL_ERROR "Clang version has not been tested for Nomad!")
    endif()
else()
    message(WARNING "You are using an unsupported compiler! Compilation has only been tested with Clang and GCC.")
endif()

set(CMAKE_POSITION_INDEPENDENT_CODE ON)

option(NOMAD_INSTALL_PREFIX "Choose where to install nomad" OFF)

set(NOMAD_HEADERS
    src/Algo_Parameters.hpp
    src/Barrier.hpp
    src/Cache.hpp
    src/Cache_File_Point.hpp
    src/Cache_Point.hpp
    src/Cache_Search.hpp
    src/Clock.hpp
    src/Direction.hpp
    src/Directions.hpp
    src/Display.hpp
    src/Double.hpp
    src/Eval_Point.hpp
    src/Evaluator.hpp
    src/Evaluator_Control.hpp
    src/Exception.hpp
    src/Extended_Poll.hpp
    src/Filter_Point.hpp
    src/GMesh.hpp
    src/LH_Search.hpp
    src/L_Curve.hpp
    src/Mads.hpp
    src/Model_Sorted_Point.hpp
    src/Model_Stats.hpp
    src/Multi_Obj_Evaluator.hpp
    src/Multi_Obj_Quad_Model_Evaluator.hpp
    src/NelderMead_Search.hpp
    src/NelderMead_Simplex_Eval_Point.hpp
    src/OrthogonalMesh.hpp
    src/Parameter_Entries.hpp
    src/Parameter_Entry.hpp
    src/Parameters.hpp
    src/Pareto_Front.hpp
    src/Pareto_Point.hpp
    src/Phase_One_Evaluator.hpp
    src/Phase_One_Search.hpp
    src/Point.hpp
    src/Priority_Eval_Point.hpp
    src/Quad_Model.hpp
    src/Quad_Model_Evaluator.hpp
    src/Quad_Model_Search.hpp
    src/RNG.hpp
    src/Random_Pickup.hpp
    src/SMesh.hpp
    src/Search.hpp
    src/Set_Element.hpp
    src/Sgtelib_Model_Evaluator.hpp
    src/Sgtelib_Model_Manager.hpp
    src/Sgtelib_Model_Search.hpp
    src/Signature.hpp
    src/Signature_Element.hpp
    src/Single_Obj_Quad_Model_Evaluator.hpp
    src/Slave.hpp
    src/Speculative_Search.hpp
    src/Stats.hpp
    src/TrendMatrix_Line_Search.hpp
    src/Uncopyable.hpp
    src/VNS_Search.hpp
    src/Variable_Group.hpp
    src/XMesh.hpp
    src/defines.hpp
    src/nomad.hpp
    src/nomad_version.hpp
    src/utils.hpp)

set(NOMAD_SOURCES
    src/Algo_Parameters.cpp
    src/Barrier.cpp
    src/Cache.cpp
    src/Cache_File_Point.cpp
    src/Cache_Point.cpp
    src/Cache_Search.cpp
    src/Clock.cpp
    src/Direction.cpp
    src/Directions.cpp
    src/Display.cpp
    src/Double.cpp
    src/Eval_Point.cpp
    src/Evaluator.cpp
    src/Evaluator_Control.cpp
    src/Extended_Poll.cpp
    src/GMesh.cpp
    src/LH_Search.cpp
    src/L_Curve.cpp
    src/Mads.cpp
    src/Model_Sorted_Point.cpp
    src/Model_Stats.cpp
    src/Multi_Obj_Evaluator.cpp
    src/NelderMead_Search.cpp
    src/NelderMead_Simplex_Eval_Point.cpp
    src/OrthogonalMesh.cpp
    src/Parameter_Entries.cpp
    src/Parameter_Entry.cpp
    src/Parameters.cpp
    src/Pareto_Front.cpp
    src/Pareto_Point.cpp
    src/Phase_One_Evaluator.cpp
    src/Phase_One_Search.cpp
    src/Point.cpp
    src/Priority_Eval_Point.cpp
    src/Quad_Model.cpp
    src/Quad_Model_Evaluator.cpp
    src/Quad_Model_Search.cpp
    src/RNG.cpp
    src/Random_Pickup.cpp
    src/SMesh.cpp
    src/Sgtelib_Model_Evaluator.cpp
    src/Sgtelib_Model_Manager.cpp
    src/Sgtelib_Model_Search.cpp
    src/Signature.cpp
    src/Slave.cpp
    src/Speculative_Search.cpp
    src/Stats.cpp
    src/TrendMatrix_Line_Search.cpp
    src/VNS_Search.cpp
    src/Variable_Group.cpp
    src/XMesh.cpp
    src/nomad.cpp
    src/utils.cpp)


#include(GNUInstallDirs)
#include(CMakePackageConfigHelpers)

#add external directories
add_subdirectory (${CMAKE_CURRENT_SOURCE_DIR}/ext)

#build shared library nomad
add_library(nomad STATIC ${NOMAD_SOURCES} ${NOMAD_HEADERS})
target_include_directories(nomad PUBLIC
    ${CMAKE_SOURCE_DIR}/ext
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/src>
    $<INSTALL_INTERFACE:${CMAKE_INSTALL_INCLUDEDIR}/nomad>)
target_link_libraries(nomad sgtelib)

#build executable
# add_executable(nomad_bin ${NOMAD_SOURCES} ${NOMAD_HEADERS})
# target_include_directories(nomad_bin PUBLIC
#     ${CMAKE_SOURCE_DIR}/nomad_sources/ext
#     $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/nomad_sources/src>
#     $<INSTALL_INTERFACE:${CMAKE_INSTALL_INCLUDEDIR}/nomad>)
# target_link_libraries(nomad_bin sgtelib)
# set_target_properties(nomad_bin PROPERTIES OUTPUT_NAME nomad)
#
# target_include_directories(PyNomad PUBLIC
#     ${CMAKE_SOURCE_DIR}/nomad_sources/ext
#     $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/nomad_sources/src>)
#     # $<INSTALL_INTERFACE:${CMAKE_INSTALL_INCLUDEDIR}/Pyomad>)
# target_link_libraries(PyNomad nomad sgtelib)
# python_extension_module(PyNomad)

# installing executables and libraries
install(TARGETS nomad
    RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
    LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
    PUBLIC_HEADER DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}/nomad)

# install header files
install(FILES ${NOMAD_HEADERS}
    DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}/nomad)
