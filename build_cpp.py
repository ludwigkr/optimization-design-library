#!/usr/bin/env python3
import os
import sys
from pathlib import Path
import pathlib

local_folder_path = os.path.dirname(__file__)
sys.path.append(local_folder_path + "/qpoases_builder")
from build_qpoases import QpoasesBuilder
from optimizationproblem import OptimizationProblem
from qpelements import QuadraticOptimizerElements

class CppBuilder:
    def __init__(self) -> None:
        self.build_qpoases = True
        pass

    def build(self, op: OptimizationProblem, path=None) -> None:
        self.quadratic_elements = QuadraticOptimizerElements(op)
        if self.build_qpoases:
            qpoases_builder = QpoasesBuilder()
            qpoases_builder.build(op, self.quadratic_elements, path)
            self.build_index(op, path)
            self.copy_dependencies(path)


    def copy_dependencies(self, path=None) -> None:
        library_path = str(pathlib.Path(__file__).parent.resolve())
        if path != None:
            cmd = 'cp ' + library_path + '/cpp/sqpmethod.* ' + library_path +'/cpp/quadraticoptimizer.h ' + path
            os.popen(cmd)
            print(cmd)


    def build_index(self, op: OptimizationProblem, path=None) -> None:
        index_header = "#pragma once\n"
        index_header += '#define ' + op.name.upper() + '_VERSION "' + str(op.version) + '"\n'
        index_header += "#define N_OPTVARS " + str(op.optvars.n_vars) + "\n"
        index_header += "#define N_CONSTRAINTS " + str(op.constraints.n_constraints) + "\n"
        index_header += op.exported_defines.code


        index_header += "\n"
        index_header += "enum optvar_idx {\n"
        for j, idxs_key in enumerate(op.optvars.idxs):
            name = op.optvars.names[j]
            idxs = op.optvars.idxs[idxs_key]
            if len(idxs) == 1:
                index_header += "    " + name + " = " + str(idxs[0, 0]) + ",\n"
            else:
                index_header += "    " + name + "_first = " + str(idxs[0, 0]) + ",\n"
                index_header += "    " + name + "_last = " + str(idxs[-1, -1]) + ",\n"
        index_header += "};\n"

        index_header += "\n"
        index_header += "enum param_idx {\n"
        for j, idxs_key in enumerate(op.problem_parameters.idxs):
            name = op.problem_parameters.names[j]
            idxs = op.problem_parameters.idxs[idxs_key]
            if len(idxs) == 1:
                index_header += "    " + name + " = " + str(idxs[0, 0]) + ",\n"
            else:
                index_header += "    " + name + "_first = " + str(idxs[0, 0]) + ",\n"
                index_header += "    " + name + "_last = " + str(idxs[-1, -1]) + ",\n"
        index_header += "};\n"

        index_header += "\n"
        index_header += "enum inequality_constraint_idx {\n"
        for j, idxs_key in enumerate(op.constraints.idxs):
            name = idxs_key
            idxs = op.constraints.idxs[idxs_key]
            if len(idxs) == 1:
                index_header += "    " + name + " = " + str(idxs[0]) + ",\n"
            else:
                index_header += "    " + name + "_first = " + str(idxs[0]) + ",\n"
                index_header += "    " + name + "_last = " + str(idxs[-1]) + ",\n"
        index_header += "};\n"


        if path is None:
            file_path = './' + op.name + "_index.h"
        else:
            file_path = Path(path + '/' + op.name + "_index.h").expanduser()
        print(file_path)
        with open(file_path, "w") as f:
            f.write(index_header)
