project(nlopt-template)
cmake_minimum_required(VERSION 2.9.0)

set(CMAKE_BUILD_TYPE Debug)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
# add_compile_options(--coverage -g -O0)
# set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} --coverage")
# set(CMAKE_SHARED_LINKER_FLAGS "${CMAKE_SHARED_LINKER_FLAGS} --coverage")

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED True)

find_package(PkgConfig REQUIRED)
find_package(CppUTest REQUIRED)
find_package(NLopt REQUIRED)
message(STATUS "Nlopt_FOUND: ${NLOPT_FOUND}")
message(STATUS "Nlopt_INCLUDE_DIRS: ${NLOPT_INCLUDE_DIRS}")
message(STATUS "Nlopt_LIBRARIES: ${NLOPT_LIBRARIES}")
message(STATUS "Nlopt_VERSION: ${NLOPT_VERSION}"    )
pkg_check_modules(EIGEN3 REQUIRED eigen3)

set(SRC_DIR ./)
set(UNITTEST_DIR ./)
include_directories(${SRC_DIR})
include_directories( ${EIGEN3_INCLUDE_DIRS} )


set(SOURCE_FILES_UNITTEST
    ${UNITTEST_DIR}/test_main.cpp
    ${UNITTEST_DIR}/test_nlopt.cpp
    ${SRC_DIR}/nlopt_example_interface.cpp
    ${SRC_DIR}/nlopt_example_formulation.cpp)

# add_executable(${PROJECT_NAME} ${SOURCE_FILES_PROGRAM})

add_executable(test_${PROJECT_NAME} ${SOURCE_FILES_UNITTEST})
target_link_libraries(test_${PROJECT_NAME} nlopt)
target_link_libraries(test_${PROJECT_NAME} CppUTest CppUTestExt)
