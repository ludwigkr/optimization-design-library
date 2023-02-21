#!/usr/bin/env python3
import sys
import casadi
import numpy as np

from variables import Variables
from optimizationproblem import OptimizationProblem

class ProblemBuildHelper:
    def __init__(self) -> None:
        self.temporary = '_temporary'
        pass

    def class_name(self, name: str) -> str:
        name = name.replace("_", " ")
        name = name.title()
        name = name.replace(" ", "")
        return name + "QuadraticOptimizer"

    def variable_structure_definition(self, name: str, var: Variables) -> str:
        # variables definition in structure
        variable_structure = "struct " + name + "{\n"
        for vi, v in enumerate(var.variables):
            if v.size1() == 1 and v.size_2() == 1:
                variable_structure += "    float " + var.names[vi] + ";\n"
            else:
                variable_structure += "    Eigen::VectorXd " + var.names[vi] + ";\n"

        # constructor header:
        variable_structure += "\n    " + name + "("
        for vi, v in enumerate(var.variables):
            if v.size1() == 1 and v.size_2() == 1:
                variable_structure += "float _" + var.names[vi] + ", "
            else:
                variable_structure += "Eigen::VectorXd _" + var.names[vi] + ", "

        if variable_structure[-2:] == ', ':
            variable_structure = variable_structure[:-2]

        variable_structure += "):\n"
        for vi, v in enumerate(var.variables):
            variable_structure += "        " + var.names[vi] + "(_" + var.names[vi] + "),\n"
        variable_structure = variable_structure[:-2]
        variable_structure += "{}\n\n"

        variable_structure += "};"
        print(variable_structure)
        return variable_structure

    def SX_sparse_str(self, mat: casadi.SX) -> str:
        tmp_file = '/tmp/opti_design_lib'
        sys.stdout = open(tmp_file,'wt')
        mat.print_sparse()
        sys.stdout = sys.__stdout__
        with open(tmp_file, "r") as f:
            ret = f.read()
        with open(tmp_file, "w"):
            pass
        ret = ret.replace(' ', '')
        ret = ret.split('\n')
        return ret

    def build_matrix_definitions(self, name, defs: [str]) -> str:
        ret = ""
        var_name = name + self.temporary
        for i, _def in enumerate(defs):
            value = _def.split('=')[-1]
            value.replace('@', var_name)
            ret += 'double ' + var_name + str(i+1) + " = " + value + ";\n"
        return ret

    def build_entry_lhs(self, name: str, idx_str: str, as_vector: bool, mat_size=0) -> str:
        """Creates the lhs formulation of an entry for a value of a matrix or a vector. E.g. H[0] , dconst(1, 0)"""
        if as_vector:
            idxs = idx_str.replace('(', '').replace(')', '').split(',')
            idx = int(idxs[0]) + mat_size * int(idxs[1])
            lhs = name + '[' + str(idx) + ']'
        else:
            lhs = name + idx_str

        return lhs

    def build_matrix_values(self, name, vals: [str], as_vector: bool, mat_size2: int)->str:
        ret = ''
        temp_name = name + self.temporary
        for v, val in enumerate(vals):
            val_components = val.split('->')
            lhs = self.build_entry_lhs(name, val_components[0], as_vector, mat_size2)
            rhs = val_components[1].replace('@', temp_name)
            ret += lhs + " = " + rhs + ';\n'

        return ret

    def build_vector_values(self, name, vals: [str], as_vector: bool) -> str:
        ret = ''
        temp_name = name + self.temporary
        for v, val in enumerate(vals):
            val_components = val.split('->')
            lhs = self.build_entry_lhs(name, val_components[0], as_vector)
            rhs = val_components[1].replace('@', temp_name)
            ret += lhs + " = " + rhs + ';\n'

        return ret

    def build_dense_matrix(self, name: str, mat: casadi.SX, as_vector=True):
        mat = casadi.SX(mat)
        smat = self.SX_sparse_str(mat)
        print(smat)
        definitions = [e.replace(',', '') for e in smat if e[0] == '@']
        values = [e for e in smat if e[0] == '(']
        print(definitions)
        print(values)
        ret = self.build_matrix_definitions(name, definitions)
        if mat.size1() == 1 or mat.size2() == 1:
            ret += self.build_vector_values(name, values, as_vector) 
        else:
            ret += self.build_matrix_values(name, values, as_vector, mat.size2())

        lines = ret.split('\n')
        indendet_lines = ["    " + l for l in lines if l != '']
        ret = "\n".join(indendet_lines)
        return ret

    def substitude_variable(self, exp: str, old_name: str, new_name: str, N: int) -> str:
        for n in reversed(range(N)):
            search_pattern = old_name + "_" + str(n)
            replace_pattern = new_name + "[" + str(n) + "]"
            exp = exp.replace(search_pattern, replace_pattern)

        return exp
        

    def substitute_variable(self, exp: str, name: str, link_symbol: str, vars: Variables) -> str:
        for v, var in enumerate(vars.names):
            N = vars.variables[v].size1() * vars.variables[v].size2()
            if N > 1:
                for n in reversed(range(N)):
                    search_pattern = var + "_" + str(n)
                    replace_pattern = name + link_symbol + var + "[" + str(n) + "]"
                    exp = exp.replace(search_pattern, replace_pattern)

        return exp

    def sustitute_parameters(self, exp: str, name: str, params: Variables) -> str:
        for p, param_name in enumerate(params.names):
            pidxs = params.idxs[param_name]
            N = np.size(pidxs)
            for n in reversed(range(N)):
                search_pattern = param_name + '_' + str(n)
                replace_pattern = name  + str(pidxs[n])
                exp = exp.replace(search_pattern, replace_pattern)

        return exp
