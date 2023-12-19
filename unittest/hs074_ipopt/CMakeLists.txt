project("hs074")
cmake_minimum_required(VERSION 3.0)

# add_compile_definitions("-g")
set(CMAKE_BUILD_TYPE Debug)

find_package(PkgConfig REQUIRED)

include_directories("../../../optimization-design-library/cpp/")
include_directories("../../../optimization-design-library/cpp/json/include/")
include_directories("/usr/include/coin")
link_directories("/usr/lib")

set(SOURCE_FILES_IPOPT_RUN
    main.cpp
    ../../../optimization-design-library/cpp/test_case_importer.cpp
    hs074_interface.cpp
    hs074_problem_ipopt.cpp
    ipopt_params.cpp)

set(SOURCE_FILES_IPOPT_UNITTEST
    test_main.cpp
    hs074_test.cpp
    ../../../optimization-design-library/cpp/test_case_importer.cpp
    hs074_interface.cpp
    hs074_problem_ipopt.cpp
    ipopt_params.cpp)

add_executable(run_${PROJECT_NAME} ${SOURCE_FILES_IPOPT_RUN})
target_link_libraries(run_${PROJECT_NAME} ipopt)

add_executable(test_${PROJECT_NAME} ${SOURCE_FILES_IPOPT_UNITTEST})
target_link_libraries(test_${PROJECT_NAME} ipopt)
target_link_libraries(test_${PROJECT_NAME} CppUTest CppUTestExt)
