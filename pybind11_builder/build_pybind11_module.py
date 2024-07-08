import numpy as np
import os
import shutil
from pathlib import Path
local_folder_path = Path(os.path.dirname(os.path.abspath(__file__)))

import sys
sys.path.append("../helpers")
import path_manager

def variable_inits(var):
    ret = ""
    if len(var.names) > 0:
        ret = ".def(py::init<>())\n"
        args = ""
        
        for i in range(len(var.names)):
            name = var.names[i]
            if np.size(var.idxs[name], 0) <= 1 and np.size(var.idxs[name], 1) <= 1:
                args += "float, "
            elif np.size(var.idxs[name], 0) <= 1 or np.size(var.idxs[name], 1) <= 1:
                args += "Eigen::VectorXd, "
            else:
                args += "Eigen::MatrixXd, "

        ret += f"    .def(py::init<{args[:-2]}>())"

    return ret

def variable_elements(var_name, var):
    ret = ""
    for element_name in var.names:
        ret += f'.def_readwrite("{element_name}", &{var_name}::{element_name})\n'
    return ret[:-1]

def export(op, path):
    with open(f"{local_folder_path}/pybind11_module_template.cpp", "r") as f:
        ret = f.read()

    class_name = path_manager.class_name(op.name)
    lower_name = class_name.lower()
    ret = ret.replace('Optproblem', class_name)
    ret = ret.replace('optproblem', op.name)

    ret = ret.replace("/** SCENARIO PARAMETER INITIALIZATIONS */", variable_inits(op.scenario_parameters))
    ret = ret.replace("/** PROBLEM PARAMETER INITIALIZATIONS */", variable_inits(op.problem_parameters))
    ret = ret.replace("/** OPTIMIZED VARIABLE INITIALIZATIONS */", variable_inits(op.optvars))
    ret = ret.replace("/** SCENARIO PARAMETER ELEMENTS */", variable_elements("scenario_parameter", op.scenario_parameters))
    ret = ret.replace("/** PROBLEM PARAMETER ELEMENTS */", variable_elements("problem_parameter", op.problem_parameters))
    ret = ret.replace("/** OPTIMIZED VARIABLE ELEMENTS */", variable_elements("optimized_variable", op.optvars))

    with open(f"./{path}/{op.name}_pymodule.cpp", "w") as f:
        f.write(ret)

def cmake_insert(op):
    class_name = path_manager.class_name(op.name)
    lower_name = class_name.lower()
    ret = "find_package(PkgConfig REQUIRED)\n"
    ret += "pkg_check_modules(EIGEN3 REQUIRED eigen3)\n"
    ret += "pkg_check_modules(IPTOPT REQUIRED ipopt)\n\n"
    ret += "add_subdirectory(../../pybind11 ..)\n\n"
    ret += "set(SOURCE_FILES_IPOPT_PYBIND11\n"
    ret += f"    {lower_name}_pymodule.cpp\n"
    ret += f"    {lower_name}_interface.cpp\n"
    ret += f"    {lower_name}_problem_ipopt.cpp\n"
    ret += "    ipopt_params.cpp)\n\n"
    ret += "pybind11_add_module(${PROJECT_NAME} ${SOURCE_FILES_IPOPT_PYBIND11})\n"
    ret += "target_link_libraries(${PROJECT_NAME} PRIVATE ipopt)"
    print(ret)
