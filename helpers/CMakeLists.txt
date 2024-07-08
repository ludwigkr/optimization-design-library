project("<problem_name>")
cmake_minimum_required(VERSION 3.0)

# add_compile_definitions("-g")
set(CMAKE_BUILD_TYPE Debug)

add_subdirectory(../optimization-design-library/pybind11_builder/pybind11 ..)

find_package(PkgConfig REQUIRED)
pkg_check_modules(EIGEN3 REQUIRED eigen3)
pkg_check_modules(IPTOPT REQUIRED ipopt)

include_directories( ${EIGEN3_INCLUDE_DIRS} )

include_directories("../../../optimization-design-library/cpp/")
include_directories("../../../optimization-design-library/cpp/json/include/")
include_directories("/usr/include/coin")
link_directories("/usr/lib")

set(SOURCE_FILES_IPOPT_RUN
    main.cpp
    ../../../optimization-design-library/cpp/test_case_importer.cpp
    <problem_name>_interface.cpp
    <problem_name>_problem_ipopt.cpp
    ipopt_params.cpp)

set(SOURCE_FILES_IPOPT_UNITTEST
    test_main.cpp
    <problem_name>_test.cpp
    ../../../optimization-design-library/cpp/test_case_importer.cpp
    <problem_name>_interface.cpp
    <problem_name>_problem_ipopt.cpp
    ipopt_params.cpp)

set(SOURCE_FILES_IPOPT_PYBIND11
    <problem_name>_pymodule.cpp
    <problem_name>_interface.cpp
    <problem_name>_problem_ipopt.cpp
    ipopt_params.cpp
)

add_executable(run_${PROJECT_NAME} ${SOURCE_FILES_IPOPT_RUN})
target_link_libraries(run_${PROJECT_NAME} ipopt)

add_executable(test_${PROJECT_NAME} ${SOURCE_FILES_IPOPT_UNITTEST})
target_link_libraries(test_${PROJECT_NAME} ipopt)
target_link_libraries(test_${PROJECT_NAME} CppUTest CppUTestExt)

pybind11_add_module(py${PROJECT_NAME} ${SOURCE_FILES_IPOPT_PYBIND11})
target_link_libraries(py${PROJECT_NAME} PRIVATE ipopt)