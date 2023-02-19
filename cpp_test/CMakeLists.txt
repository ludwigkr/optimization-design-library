set(LIB_MAJOR_VERSION "1")
set(LIB_MINOR_VERSION "0")
set(LIB_PATCH_VERSION "0")
set(LIB_VERSION_STRING "${LIB_MAJOR_VERSION}.${LIB_MINOR_VERSION}.${LIB_PATCH_VERSION}")

if (CMAKE_VERSION VERSION_LESS 3.0)
project(cpp-test CXX)
else()
  cmake_policy(SET CMP0048 NEW)
  PROJECT(cpp-test VERSION "${LIB_VERSION_STRING}" LANGUAGES CXX)
endif()

cmake_minimum_required(VERSION 3.10.2)
find_package(PkgConfig REQUIRED)
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

if(NOT CMAKE_BUILD_TYPE)
  set(CMAKE_BUILD_TYPE Debug)
endif()
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -lstdc++fs -Wall -Wextra -Wlogical-op -Wuseless-cast -Wold-style-cast -Wdouble-promotion -Wshadow -Wformat=2  -Wno-missing-field-initializers")
MESSAGE( STATUS "CMAKE BUILD TYPE: " ${CMAKE_BUILD_TYPE} )


find_package(osqp REQUIRED)
if(OPTI_ROSVIS)
  find_package(roscpp REQUIRED)
  find_package(std_msgs REQUIRED)
  find_package(tf2 REQUIRED)
  find_package(tf2_ros REQUIRED)
endif()

pkg_check_modules(CASADI REQUIRED casadi)

message("CASADI_LIBRARY_DIRS: ${CASADI_LIBRARY_DIRS}")
message("CASADI_LIBRARIES: ${CASADI_LIBRARIES}")
message("CASADI_INCLUDEDIR: ${CASADI_INCLUDEDIR}")
set(CMAKE_CXX_LINK_EXECUTABLE "${CMAKE_CXX_LINK_EXECUTABLE} -ldl")


option(USE_OSQP "use_osqp" 0)
option(USE_QPOASES "use_qpoases" 1)

if(USE_OSQP AND USE_QPOASES)
            set(USE_OSQP 0)
            set(USE_QPOASES 1)
            message("Two optimizer libaries select, while only one is supported at the same time. Enable osqp by disabling qpoases at the same time.")
endif()

if(USE_OSQP)
  add_definitions(-DUSE_OSQP)
  remove_definitions(-DUSE_QPOASES)
  message("Set -DUSE_OSQP")
endif(USE_OSQP)

if(USE_QPOASES)
  remove_definitions(-DUSE_OSQP)
  add_definitions(-DUSE_QPOASES)
  message("Set -DUSE_QPOASES")
endif(USE_QPOASES)

set(SRC_FILES  main.cpp
                  # ocptester.cpp
                  minnlptest.cpp
                  min_nlp_interface.cpp
                  ../min_nlp/min_nlp_quad_opti_qpoases.cpp
                  ../cpp/sqpmethod.cpp
                  ../cpp/qpoasesconfig.cpp
)


add_executable(${PROJECT_NAME} ${SRC_FILES})

target_include_directories(${PROJECT_NAME} PRIVATE ./)
target_include_directories(${PROJECT_NAME} PRIVATE ../cpp)
target_include_directories(${PROJECT_NAME} PRIVATE ../min_nlp)
target_include_directories(${PROJECT_NAME} PRIVATE ../min_nlp_with_params)

target_include_directories(${PROJECT_NAME} SYSTEM PRIVATE ~/repos/qpOASES/include)
target_include_directories(${PROJECT_NAME} SYSTEM PRIVATE ${CASADI_INCLUDE_DIR})

target_link_libraries(${PROJECT_NAME} ${OpenCV_LIBS} CppUTest CppUTestExt)
target_link_libraries(${PROJECT_NAME} qpOASES)
target_link_libraries(${PROJECT_NAME} ${CASADI_LIBRARIES})
target_link_libraries(${PROJECT_NAME} osqp::osqp)
target_link_libraries(${PROJECT_NAME} osqp::osqpstatic)


# add_custom_command(OUTPUT ${CMAKE_CURRENT_SOURCE_DIR}/../ocp_design/min_nlp/min_nlp_quadratic_optimizer.cpp ${CMAKE_CURRENT_SOURCE_DIR}/../ocp_design/tti/tti_quadratic_optimizer.cpp ${CMAKE_CURRENT_SOURCE_DIR}/../ocp_design/intercept_in_planes/intercept_in_planes_quadratic_optimizer.cpp DEPENDS ${CMAKE_CURRENT_SOURCE_DIR}/../ocp_design/casadi_parser/solvertemplate_osqp.cpp ${CMAKE_CURRENT_SOURCE_DIR}/../ocp_design/casadi_parser/solvertemplate_osqp.h ${CMAKE_CURRENT_SOURCE_DIR}/../ocp_design/casadi_parser/solvertemplate_qpoases.cpp ${CMAKE_CURRENT_SOURCE_DIR}/../ocp_design/casadi_parser/solvertemplate_qpoases.h ${CMAKE_CURRENT_SOURCE_DIR} ./../ocp_design/intercept_in_planes/ocp_intercept_in_planes.py ${CMAKE_CURRENT_SOURCE_DIR}/../ocp_design/tti/ocp_tti.py
#                    COMMAND make all
#                    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/../ocp_design/
# )
