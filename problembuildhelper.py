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

    def class_name(self, name: str, quadratic_optimier=False) -> str:
        name = name.replace("_", " ")
        name = name.title()
        name = name.replace(" ", "")
        if quadratic_optimier:
            name = name + "QuadraticOptimizer"
        return name

    def variable_structure_definition(self, name: str, var: Variables) -> str:
        # variables definition in structure
        variable_structure = "struct " + name + "{\n"
        for vi, v in enumerate(var.variables):
            if v.size1() == 1 and v.size2() == 1:
                variable_structure += "    float " + var.names[vi] + ";\n"
            else:
                variable_structure += "    Eigen::VectorXd " + var.names[vi] + ";\n"

        # constructor header:
        variable_structure += "\n    " + name + "("
        for vi, v in enumerate(var.variables):
            if v.size1() == 1 and v.size2() == 1:
                variable_structure += "float _" + var.names[vi] + ", "
            else:
                variable_structure += "Eigen::VectorXd _" + var.names[vi] + ", "

        if variable_structure[-2:] == ', ':
            variable_structure = variable_structure[:-2]

        variable_structure += "):\n"
        for vi, v in enumerate(var.variables):
            variable_structure += "        " + var.names[vi] + "(_" + var.names[vi] + "),\n"
        variable_structure = variable_structure[:-2]
        variable_structure += "{}\n\n    "
        variable_structure += name+"(){}\n\n"

        variable_structure += "};"
        return variable_structure

    def SX_sparse_str(self, mat: casadi.SX) -> str:
        tmp_file = '/tmp/opti_design_lib'
        with open(tmp_file,'wt') as sys.stdout:
        # sys.stdout = open(tmp_file,'wt')
            mat.print_sparse()
        sys.stdout = sys.__stdout__
        with open(tmp_file, "r") as f:
            ret = f.read()
        with open(tmp_file, "w"):
            pass
        ret = ret.replace(' ', '')
        ret = ret.split('\n')
        return ret
    
    def SX_dense_str(self, mat: casadi.SX) -> str:
        tmp_file = '/tmp/opti_design_lib'
        with open(tmp_file,'wt') as sys.stdout:
        # sys.stdout = open(tmp_file,'wt')
            mat.print_dense()
        sys.stdout = sys.__stdout__
        with open(tmp_file, "r") as f:
            ret = f.read()
        with open(tmp_file, "w"):
            pass
        # ret = ret.replace(' ', '')
        ret = ret.split(',')
        return ret

    def build_matrix_definitions(self, name, defs: [str]) -> str:
        ret = ""
        var_name = name + self.temporary
        for i, _def in enumerate(defs):
            value = _def.split('=')[-1]
            value = value.replace('@', var_name)
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

    def build_matrix_values_dense(self, name, vals: [str], as_vector):
        ret = ''
        row = 0
        column = 0
        temp_name = name + self.temporary
        for v, val in enumerate(vals):
            original_val = val
            val = val.replace('[','').replace(']','').replace('\n','').replace(' ', '').replace('00', '0')
            if as_vector:
                ret += f"{name}[{column}] = {val};\n"
            else:
                ret += f"{name}[{row},{column}] = {val};\n"

            column += 1

            if ']' in original_val:
                if not as_vector:
                    column = 0
                row += 1

        ret = ret.replace("@", temp_name)
        return ret

    def build_vector_values(self, name, vals: [str], as_vector: bool) -> str:
        ret = ''
        temp_name = name + self.temporary
        for v, val in enumerate(vals):
            val_components = val.split('->')
            lhs = self.build_entry_lhs(name, val_components[0], as_vector, 1)
            rhs = val_components[1].replace('@', temp_name)
            ret += lhs + " = " + rhs + ';\n'

        return ret

    def build_matrix(self, name: str, mat: casadi.SX, as_vector=True, dense=False):
        mat = casadi.SX(mat)
        if not dense:
            smat = self.SX_sparse_str(mat)
            definitions = [e.replace(',', '') for e in smat if e[0] == '@']
            values = [e for e in smat if e[0] == '(']
            ret = self.build_matrix_definitions(name, definitions)
            if mat.size1() == 1 or mat.size2() == 1:
                ret += self.build_vector_values(name, values, as_vector)
            else:
                ret += self.build_matrix_values(name, values, as_vector, mat.size2())

        else:
            smat = self.SX_dense_str(mat)
            definitions = [e for e in smat if e[0] == '@']
            values = [e for e in smat if e[0] != '@']
            ret = self.build_matrix_definitions(name, definitions)
            ret += self.build_matrix_values_dense(name, values, as_vector)

        lines = ret.split('\n')
        indendet_lines = ["    " + l for l in lines if l != '']
        ret = "\n".join(indendet_lines)
        return ret

    def substitude_variable(self, exp: str, old_name: str, new_name: str, N: int, index_offset=0) -> str:
        if N == 1:
            search_pattern = old_name
            replace_pattern = new_name + "[" + str(index_offset) + "]"
            exp = exp.replace(search_pattern, replace_pattern)

        else:
            for n in reversed(range(N)):
                search_pattern = old_name + "_" + str(n)
                replace_pattern = new_name + "[" + str(n + index_offset) + "]"
                exp = exp.replace(search_pattern, replace_pattern)

        return exp

    def substitute_variable_in_struct(self, exp: str, sturct_name: str, link_symbol: str, vars: Variables) -> str:
        for v, var in enumerate(vars.names):
            N = vars.variables[v].size1() * vars.variables[v].size2()
            if N > 1:
                for n in reversed(range(N)):
                    search_pattern = var + "_" + str(n)
                    replace_pattern = sturct_name + link_symbol + var + "[" + str(n) + "]"
                    exp = exp.replace(search_pattern, replace_pattern)
            else:
                search_pattern = var
                replace_pattern = sturct_name + link_symbol + var
                exp = exp.replace(search_pattern, replace_pattern)

        return exp

    def subsitude_variables(self, exp: str, op: OptimizationProblem, prob_param_as_struct=False) -> str:

        ret = exp
        for optvar_name in op.optvars.names:
            ret = self.substitude_variable(ret, optvar_name, 'xopt', op.optvars.idxs[optvar_name].size, op.optvars.idxs[optvar_name][0,0])

        if prob_param_as_struct:
            ret = self.substitute_variable_in_struct(ret, "prob_param", "->", op.problem_parameters)
        else:
            for param_name in op.problem_parameters.names:
                ret = self.substitude_variable(ret, param_name, 'param', op.problem_parameters.idxs[param_name].size, op.problem_parameters.idxs[param_name][0,0])

        ret = self.substitude_variable(ret, 'lamg', 'lamg', op.constraints.n_constraints)
        ret = self.substitute_variable_in_struct(ret, 'scenario', '->', op.scenario_parameters)
        return ret

    def build_vectormatrix_for_optimizer_formulation(self, op: OptimizationProblem, vectormatrix_name:str, vectormatrix_casadi_formulation:casadi.SX, as_vector=False, dense=False):
        ret = self.build_matrix(vectormatrix_name, vectormatrix_casadi_formulation, as_vector=as_vector, dense=dense)
        ret = self.subsitude_variables(ret, op).replace("prob_param", "param")
        return ret

    def build_scalar_for_optimizer_formulation(self, op: OptimizationProblem, vectormatrix_name:str, vectormatrix_casadi_formulation:casadi.SX, as_vector=False, dense=False):
        ret = self.build_matrix(vectormatrix_name, vectormatrix_casadi_formulation, as_vector=as_vector, dense=dense)
        ret = self.subsitude_variables(ret, op).replace("prob_param", "param")
        ret = ret.replace("(0,0)", "")
        ret = ret.replace("(0)", "")

        ret_split = ret.split("=")
        val_name = ret_split[0].split("[")[0].replace(" ", "")
        ret = val_name + " = " + ret_split[1]
        return ret

    def build_ipopt_index(self, op: OptimizationProblem, vector_matrix_casadi_formulation: casadi.SX):
        ret = ""
        smat = self.SX_sparse_str(vector_matrix_casadi_formulation)
        value_lines = [e for e in smat if e[0] == '(']
        for l, line in enumerate(value_lines):
            index_str = line.split("->")[0].replace("(", "").replace(")", "").split(",")
            row = int(index_str[0])
            column = int(index_str[1])
            ret += f"        iRow[{l}] = {row};\n"
            ret += f"        jCol[{l}] = {column};\n"
        return ret

    def build_ipopt_values(self, op: OptimizationProblem, vector_matrix_casadi_formulation: casadi.SX):
        # vector_matrix_casadi_formulation = casadi.reshape(vector_matrix_casadi_formulation, (-1, 1))
        # smat = self.SX_dense_str(vector_matrix_casadi_formulation)
        # define_str = [e for e in smat if e[0] == '@']
        # ret = self.build_matrix_definitions("values", define_str)

        # value_lines = [e for e in smat if e[0] == '(']
        ret = self.build_matrix("values", vector_matrix_casadi_formulation, True, False) 
        ret = self.subsitude_variables(ret, op).replace("prob_param", "param")
        
        lines = ret.split('\n')
        indendet_lines = ["    " + l for l in lines if l != '']
        ret = "\n".join(indendet_lines)
        return ret
