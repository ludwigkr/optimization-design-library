#!/usr/bin/env python3
import sys
import casadi
import re

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
        if len(var.variables) > 0:
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
            variable_structure += name+"(){\n"
            for vi, v in enumerate(var.variables):
                if v.size1() == 1 and v.size2() == 1:
                    # variable_structure += "          float _" + var.names[vi] + ", "
                    pass
                else:
                    variable_structure += f"          {var.names[vi]} = Eigen::VectorXd({v.size(1)*v.size(2)});\n"

            variable_structure += "}\n\n"

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
            definitions = [e for e in smat if e[0] == '@' or (e[0:2]==' @' and ']' not in e)]
            values = [e for e in smat if (e[0] != '@' and e[0:2] != ' @') or ']' in e]
            ret = self.build_matrix_definitions(name, definitions)
            ret += self.build_matrix_values_dense(name, values, as_vector)

        lines = ret.split('\n')
        indendet_lines = ["    " + l for l in lines if l != '']
        ret = "\n".join(indendet_lines)
        return ret

    def substitude_variable(self, exp: str, old_name: str, new_name: str, N: int, index_offset=0) -> str:
        if N == 1:
            search_pattern = "(?!_\w+)" + old_name + "(?!_\w+)"
            replace_pattern = new_name + "[" + str(index_offset) + "]"
            exp = re.sub(search_pattern, replace_pattern, exp)

        else:
            for n in reversed(range(N)):
                search_pattern = "(?!_\w+)" + old_name + "_" + str(n)+ "(?!_\w+)"
                replace_pattern = new_name + "[" + str(n + index_offset) + "]"
                exp = re.sub(search_pattern, replace_pattern, exp)

        return exp

    def substitute_variable_in_struct(self, exp: str, sturct_name: str, link_symbol: str, vars: Variables) -> str:
        for v, var in enumerate(vars.names):
            N = vars.variables[v].size1() * vars.variables[v].size2()
            if N > 1:
                for n in reversed(range(N)):
                    search_pattern = "(?!_\w+)" + var + "_" + str(n)+ "(?!_\w+)"
                    replace_pattern = sturct_name + link_symbol + var + "[" + str(n) + "]"
                    exp = re.sub(search_pattern, replace_pattern, exp)
            else:
                search_pattern = "(?!_\w+)" + var + "(?!_\w+)"
                replace_pattern = sturct_name + link_symbol + var
                exp = re.sub(search_pattern, replace_pattern, exp)

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

    def build_vectormatrix_for_optimizer_formulation(self, op: OptimizationProblem, vectormatrix_name:str, vectormatrix_casadi_formulation:casadi.SX, as_vector=False, dense=False, prob_param_as_struct=False):
        ret = self.build_matrix(vectormatrix_name, vectormatrix_casadi_formulation, as_vector=as_vector, dense=dense)
        ret = self.subsitude_variables(ret, op, prob_param_as_struct=prob_param_as_struct)
        if not prob_param_as_struct:
            ret = ret.replace("prob_param", "param")
        return ret

    def remove_matrix_information_lhs(self, exp: str) -> str:
        exp_split = exp.split("=")
        val_name = exp_split[0].split("[")[0].replace(" ", "")
        exp = val_name + " = " + exp_split[1]
        return exp

    def build_scalar_for_optimizer_formulation(self, op: OptimizationProblem, vectormatrix_name:str, vectormatrix_casadi_formulation:casadi.SX, as_vector=False, dense=False, prob_param_as_struct=False):
        ret = self.build_matrix(vectormatrix_name, vectormatrix_casadi_formulation, as_vector=as_vector, dense=dense)
        ret = self.subsitude_variables(ret, op, prob_param_as_struct=prob_param_as_struct)
        if not prob_param_as_struct:
            ret = ret.replace("prob_param", "param")
        ret = ret.replace("(0,0)", "")
        ret = ret.replace("(0)", "")

        lines = ret.split("\n")
        if len(lines)>1:
            lines[-1] = self.remove_matrix_information_lhs(lines[-1])
            ret = "\n".join(lines)
        else:
            ret = self.remove_matrix_information_lhs(ret)

        return ret

    def build_ipopt_index(self, op: OptimizationProblem, vector_matrix_casadi_formulation: casadi.SX, only_lower_triangular=False):
        ret = ""
        smat = self.SX_sparse_str(vector_matrix_casadi_formulation)
        value_lines = [e for e in smat if e[0] == '(']
        line_index = 0
        for l, line in enumerate(value_lines):
            index_str = line.split("->")[0].replace("(", "").replace(")", "").split(",")
            row = int(index_str[0])
            column = int(index_str[1])
            if not only_lower_triangular:
                ret += f"        iRow[{l}] = {row};\n"
                ret += f"        jCol[{l}] = {column};\n"

            elif only_lower_triangular and column <= row:
                if str(vector_matrix_casadi_formulation[row, column]) != 0:
                    ret += f"        iRow[{line_index}] = {row};\n"
                    ret += f"        jCol[{line_index}] = {column};\n"
                    line_index += 1
        return ret

    def correct_value_index_for_sparse_representation(self, formulation: str) -> str:

        lines = formulation.split('\n');

        idx = 0
        for i, val in enumerate(lines):
            line_parts = val.split(' = ')
            if line_parts[0][0:10] == '    values':
                lines[i] = lines[i].replace(line_parts[0], f'    values[{idx}]')
                idx += 1

        ret = "\n".join(lines)
        return ret

    def build_ipopt_values(self, op: OptimizationProblem, vector_matrix_casadi_formulation: casadi.SX, only_lower_triangular=False):
        # vector_matrix_casadi_formulation = casadi.reshape(vector_matrix_casadi_formulation, (-1, 1))
        # smat = self.SX_dense_str(vector_matrix_casadi_formulation)
        # define_str = [e for e in smat if e[0] == '@']
        # ret = self.build_matrix_definitions("values", define_str)

        # value_lines = [e for e in smat if e[0] == '(']
        vector_matrix_casadi_formulation = casadi.reshape(vector_matrix_casadi_formulation, (-1,1))
        nnz = 0
        if only_lower_triangular:
            for i in range(vector_matrix_casadi_formulation.size(1)):
                if str(vector_matrix_casadi_formulation[i]) == "0":
                    nnz += 1

            new_formulation = casadi.SX.sym('tmp', vector_matrix_casadi_formulation.size(1) - nnz, 1)
            idx = 0
            for i in range(vector_matrix_casadi_formulation.size(1)):
                if str(vector_matrix_casadi_formulation[i]) != "0":
                    new_formulation[idx] = vector_matrix_casadi_formulation[i]
                    idx += 1
            vector_matrix_casadi_formulation = new_formulation

        ret = self.build_matrix("values", vector_matrix_casadi_formulation, True, False)
        ret = self.correct_value_index_for_sparse_representation(ret)
        ret = self.subsitude_variables(ret, op, prob_param_as_struct=True)

        lines = ret.split('\n')
        indendet_lines = ["    " + l for l in lines if l != '']
        ret = "\n".join(indendet_lines)
        return ret


    def build_struct_of_variable(self, struct_name: str, vars: Variables, vector_name='x', pointer=False):
        connector = "."
        if pointer:
            connector = "->"

        ret = ""
        idx = 0
        for n, name in enumerate(vars.names):
            if vars.variables[n].size(1)*vars.variables[n].size(2) == 1:
                    ret += f"    {struct_name}{connector}{name} = {vector_name}[{idx}];\n"
                    idx += 1
            else:
                if vars.variables[n].size(1) == 1 or vars.variables[n].size(2) == 1:
                    if vars.variables[n].size(1) == 1:
                        vars.variables[n] = vars.variables[n].T

                    for v in range(vars.variables[n].size(1)):
                        ret += f"    {struct_name}{connector}{name}[{v}] = {vector_name}[{idx}];\n"
                        idx += 1
                else:
                    for v in range(vars.variables[n].size(1)):
                        for w in range(vars.variables[n].size(2)):
                            ret += f"    {struct_name}{connector}{name}[{v}, {w}] = {vector_name}[{idx}];\n"
                            idx += 1
        return ret
    
    def build_osstreams(self, op:OptimizationProblem) -> str:
        ret = "std::ostream& operator<<(std::ostream& os, const scenario_parameter& s) {\n"
        ret += '   return os << "{ scenario - '
        for name in op.scenario_parameters.names:
            if len(op.scenario_parameters.idxs[name]) > 1:
                ret += f'{name}: " << s.{name}.transpose() << ", "'
            else:
                ret += f'{name}: " << s.{name} << ", "'

        ret = ret[:-4]
        ret += ' " };";\n'
        ret += "};\n\n"

        ret += "std::ostream& operator<<(std::ostream& os, const problem_parameter& p) {\n"
        ret += '   return os << "{ prob_param - '
        for name in op.problem_parameters.names:
            if len(op.problem_parameters.idxs[name]) > 1:
                ret += f'{name}: " << p.{name}.transpose() << ", "'
            else:
                ret += f'{name}: " << p.{name} << ", "'

        ret = ret[:-4]
        ret += ' " };";\n'
        ret += "};\n\n"

        ret += "std::ostream& operator<<(std::ostream& os, const optimized_variable& o) {\n"
        ret += '   return os << "{ xopt - '
        for name in op.optvars.names:
            if len(op.optvars.idxs[name]) > 1:
                ret += f'{name}: " << o.{name}.transpose() << ", "'
            else:
                ret += f'{name}: " << o.{name} << ", "'

        ret = ret[:-4]
        ret += ' " };";\n'
        ret += "};\n\n"

        return ret

    
    def build_mappers(self, op:OptimizationProblem) -> str:

        ret = "std::tuple<std::map<std::string, size_t>, std::map<std::string, size_t>, std::map<std::string, size_t>> mappers(){\n"
        ret += "    std::map<std::string, size_t> map_scenario;\n"
        ret += "    std::map<std::string, size_t> map_prob_param;\n"
        ret += "    std::map<std::string, size_t> map_xopt;\n\n"


        for name in op.scenario_parameters.names:
            ret += f'    map_scenario["{name}"] = offsetof(scenario_parameter, {name});\n'
        ret += "\n"

        for name in op.problem_parameters.names:
            ret += f'    map_prob_param["{name}"] = offsetof(problem_parameter, {name});\n'
        ret += "\n"

        for name in op.optvars.names:
            ret += f'    map_xopt["{name}"] = offsetof(optimized_variable, {name});\n'
        ret += "\n"
        
        ret += "    return std::tuple(map_scenario, map_prob_param, map_xopt);\n"
        ret += "};"
        return ret