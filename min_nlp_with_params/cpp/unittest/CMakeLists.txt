project("min_nlp_with_params")
cmake_minimum_required(VERSION 3.0)

set(CMAKE_BUILD_TYPE Debug)

find_package(PkgConfig REQUIRED)

include_directories("../")
include_directories("../../../cpp/json/include")
include_directories("../../../cpp")
include_directories("/usr/include/coin")
link_directories("/usr/lib")


set(SOURCE_FILES_IPOPT_TEST
    main.cpp
    ../min_nlp_with_params_interface.cpp
    ../min_nlp_with_params_problem_ipopt.cpp)

add_executable(${PROJECT_NAME}_main ${SOURCE_FILES_IPOPT_TEST})
target_link_libraries(${PROJECT_NAME}_main ipopt)

set(SOURCE_FILES_IPOPT_TEST
    ./test_main.cpp
    ../../../cpp/test_case_importer.cpp
    ./test_min_nlp_with_params.cpp
    ../min_nlp_with_params_interface.cpp
    ../min_nlp_with_params_problem_ipopt.cpp)

add_executable(${PROJECT_NAME}_test ${SOURCE_FILES_IPOPT_TEST})
target_link_libraries(${PROJECT_NAME}_test ipopt)
target_link_libraries(${PROJECT_NAME}_test CppUTest CppUTestExt)
