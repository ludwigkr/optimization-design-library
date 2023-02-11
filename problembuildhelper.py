#!/usr/bin/env python3
import sys
import casadi

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
        variable_structure = variable_structure[:-2]

        variable_structure += "):\n"
        for vi, v in enumerate(var.variables):
            variable_structure += "        " + var.names[vi] + "(_" + var.names[vi] + "),\n"
        variable_structure = variable_structure[:-2]
        variable_structure += "{}\n\n"

        variable_structure += "};"
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
            ret += 'float ' + var_name + str(i+1) + " = " + value + ";\n"
        return ret

    def build_matrix_values(self, name, vals: [str])->str:
        ret = ''
        temp_name = name + self.temporary
        for v, val in enumerate(vals):
            entry = val.split('->')[1]
            lhs = name + '[' + str(v) +']'
            rhs = entry.replace('@', temp_name)
            ret += lhs + " = " + rhs + ';\n'

        return ret

    def build_vector_values(self, name, vals: [str]) -> str:
        ret = ''
        temp_name = name + self.temporary
        for i, val in enumerate(vals):
            [sidxs, entry] = val.split('->')
            sidxs = sidxs.replace('(', '').replace(')','')
            sidxs = sidxs.split(',')[1]
            sidxs = "[" + sidxs + "]"
            lhs = name + sidxs
            rhs = entry.replace('@', temp_name)
            ret += lhs + " = " + rhs + ';\n'

        return ret

    def build_dense_matrix(self, name: str, mat: casadi.SX):
        smat = self.SX_sparse_str(mat)
        print(smat)
        definitions = [e.replace(',', '') for e in smat if e[0] == '@']
        values = [e for e in smat if e[0] == '(']
        print(definitions)
        print(values)
        ret = self.build_matrix_definitions(name, definitions)
        if mat.size1() == 1 or mat.size2() == 1:
            ret += self.build_vector_values(name, values) 
        else:
            ret += self.build_matrix_values(name, values)

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
