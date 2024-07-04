#!/usr/bin/env python3
import os
import sys
import casadi
import shutil
from pathlib import Path

local_folder_path = Path(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(str(local_folder_path.parent))
sys.path.append(str(local_folder_path.parent) + "/helpers")
from optimizationproblem import OptimizationProblem
from quadratic_optimizer_elements import QuadraticOptimizerElements
import cpp_struct_definition
import cpp_struct_functions
import math_helper
import path_manager
import scalar_expression_parser
import dense_expression_parser
import sparse_expression_parser
import substitute_variables
import cpp_optimizer_helper

class IpoptBuilder:
    def __init__(self) -> None:
        pass

    def build(self, op: OptimizationProblem, path:str) -> None:
        op.build_lagrangian()
        qoe = QuadraticOptimizerElements(op)
        self.build_problem_header(op, path)
        self.build_problem_source(op, qoe, path)
        self.build_interface_header(op, path)
        self.build_interface_source(op, path)
        shutil.copy(str(local_folder_path) + "/ipopt_params.h", path)
        shutil.copy(str(local_folder_path) + "/ipopt_params.cpp", path)

    def build_interface_header(self, op: OptimizationProblem, path: str) -> None:
            with open(str(local_folder_path) + '/problem_interface.h', 'r') as f:
                header = f.read()

            class_name = path_manager.class_name(op.name)
            header = header.replace("Problem", class_name)
            header = header.replace("problem_formulation", op.name+"_problem")

            if path is None:
                file_path = './' + op.name + "_interface.h"
            else:
                file_path = Path(path + '/' + op.name + "_interface.h").expanduser()
            print(file_path)
            with open(file_path, "w") as f:
                f.write(header)

    def build_interface_source(self, op: OptimizationProblem, path: str):
            with open(str(local_folder_path) + '/problem_interface.cpp', 'r') as f:
                source = f.read()

            class_name = path_manager.class_name(op.name)
            source = source.replace("Problem", class_name)
            source = source.replace("problem_formulation", op.name)

            if path is None:
                file_path = './' + op.name + "_interface.cpp"
            else:
                file_path = Path(path + '/' + op.name + "_interface.cpp").expanduser()
            print(file_path)
            with open(file_path, "w") as f:
                f.write(source)


    def build_problem_header(self, op: OptimizationProblem, path: str) -> None:
            with open(str(local_folder_path) + '/problem_template.h', 'r') as f:
                header = f.read()
            if path is None:
                file_path = './' + op.name + "_problem_ipopt.h"
            else:
                file_path = Path(path + '/' + op.name + "_problem_ipopt.h").expanduser()

            folder_path = os.path.dirname(file_path)
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)

            print(file_path)
            with open(file_path, "w") as f:
                f.write(header)

            n_xopts = op.optvars.n_vars
            n_constraints = op.constraints.n_constraints
            n_params = op.problem_parameters.n_vars
            class_name = path_manager.class_name(op.name)
            header = header.replace("N_DIMS_H", str(n_xopts**2))
            header = header.replace("N_DIMS_A", str(n_xopts*n_constraints))
            header = header.replace("N_XOPTS", str(n_xopts))
            header = header.replace("N_PARAMS", str(n_params))
            header = header.replace("N_CONSTRAINTS", str(n_constraints))
            header = header.replace("Problem", class_name)
            header = header.replace("struct scenario_parameter;", cpp_struct_definition.cpp_struct_definition("scenario_parameter", op.scenario_parameters))
            header = header.replace("struct problem_parameter;", cpp_struct_definition.cpp_struct_definition("problem_parameter", op.problem_parameters))
            header = header.replace("struct optimized_variable;", cpp_struct_definition.cpp_struct_definition("optimized_variable", op.optvars))

            if path is None:
                file_path = './' + op.name + "_problem_ipopt.h"
            else:
                file_path = Path(path + '/' + op.name + "_problem_ipopt.h").expanduser()
            print(file_path)
            with open(file_path, "w") as f:
                f.write(header)

    def build_problem_source(self, op: OptimizationProblem, qoe: QuadraticOptimizerElements, path: str) -> None:
        n_constraints = op.constraints.n_constraints
        n_xopts = op.optvars.n_vars


        with open(str(local_folder_path) + '/problem_template.cpp', 'r') as f:
            source = f.read()

        source = source.replace("solvertemplate", op.name +"_quad_opti_qpoases")
        class_name = path_manager.class_name(op.name)

        source = source.replace("formulation", op.name)
        source = source.replace('#include "problem_index.h"', '#include "' + str(op.name) + '_index.h"')
        source = source.replace("Problem", class_name)
        source = source.replace("N_XOPTS + N_CONSTRAINTS", str(n_xopts + n_constraints))
        source = source.replace("N_XOPTS", str(n_xopts))
        source = source.replace("N_CONSTRAINTS", str(n_constraints))
        source = source.replace("N_PARAMS", str(op.problem_parameters.n_vars))


        objective = self.build_objective(op)
        source = source.replace("/* OBJECTIVE PLACEHOLDER*/",  objective)

        objective_jacobian = self.build_objective_jacobian(op)
        source = source.replace("    /* OBJECTIVE_JACOBIAN PLACEHOLDER*/", objective_jacobian)

        [idx, values, nnz] = self.build_sparse_constraint_jacobian(op)
        source = source.replace("        /* CONSTRAINTS_JACOBIAN_SPARSE_INDEX PLACEHOLDER*/", idx)
        source = source.replace("        /* CONSTRAINTS_JACOBIAN_SPARSE_VALUES PLACEHOLDER*/", values)
        source = source.replace("CONSTRAINTS_JACOBIAN_NNZ", str(nnz))


        [lagrangian_hessian_idx, lagrangian_hessian_value, lagrangian_hessian_nnz] = self.build_sparse_lagrange_hessian(op)
        source = source.replace("        /* LAGRANGIAN_HESSIAN_SPARSE_INDEX PLACEHOLDER*/", lagrangian_hessian_idx)
        source = source.replace("        /* LAGRANGIAN_HESSIAN_SPARSE_VALUES PLACEHOLDER*/", lagrangian_hessian_value)
        source = source.replace("LAGRANGE_HESSIAN_NNZ", str(lagrangian_hessian_nnz))

        write_back_solution = cpp_struct_functions.assign_vector_values_to_struct_entries("x", "xopt", op.optvars, pointer=True)
        source = source.replace("    /*WRITE BACK SOLUTION PLACEHOLDER*/", write_back_solution)

        init_H = self.build_initialization_objective_hessian(op, qoe.objective_hessian)
        init_H = substitute_variables.substitute_variables(init_H, op)
        source = source.replace("    /* INIT H PLACEHOLDER*/", init_H)

        update_H = self.build_objective_hessian(op, qoe.objective_hessian)
        update_H = substitute_variables.substitute_variables(update_H, op)
        source = source.replace("    /* UPDATE H PLACEHOLDER*/", update_H)

        init_g = self.build_initialization_objective_jacobian(op, qoe.objective_jacobian)
        init_g = substitute_variables.substitute_variables( init_g, op)
        source = source.replace("    /* INIT g PLACEHOLDER*/", init_g)

        update_g = self.build_objective_jacobian(op)
        update_g = substitute_variables.substitute_variables( update_g, op)
        source = source.replace("    /* UPDATE g PLACEHOLDER*/", update_g)

        A = self.build_linearized_constraints_without_offset(op, qoe.constraints_jacobian)
        source = source.replace("    /* UPDATE A PLACEHOLDER*/", A)

        bA = self.build_linearized_constraints_offset(op, qoe.cx0minusdcx0)
        source = source.replace("    /* UPDATE bA PLACEHOLDER*/", bA)

        g = self.build_constraints(op, op.constraints.equations_flat())
        source = source.replace("    /* CONSTRAINTS PLACEHOLDER*/", g)

        H = self.build_objective_hessian(op, qoe.objective_hessian)
        source = source.replace("    /* UPDATE H PLACEHOLDER*/", H)

        dconstr = self.build_constraint_derivatives(op, qoe.constraints_jacobian)
        source = source.replace("    /* CONSTRAINT_DERIVATIVES PLACEHOLDER*/", dconstr)

        parameters = self.build_parameters(op, op.problem_parameters.variables_flat())
        source = source.replace("    /* PARAMS PLACEHOLDER*/", parameters).replace("parameters", "parameter")

        initial_guess = self.build_initial_guess(op, op.fn_initial_guess.call(), "x")
        source = source.replace("    /* INITIAL_GUESS PLACEHOLDER*/", initial_guess)

        lbx = self.build_lower_box_boundaries(op, op.fn_lbx.call())
        source = source.replace("    /* LBX PLACEHOLDER*/", lbx)

        ubx = self.build_upper_box_boundaries(op, op.fn_ubx.call())
        source = source.replace("    /* UBX PLACEHOLDER*/", ubx)

        lbg = self.build_lower_constraint_boundaries(op, op.fn_lbg.call())
        source = source.replace("    /* LOWER CONSTRAINTS BOUND PLACEHOLDER*/", lbg)

        ubg = self.build_upper_constraint_boundaries(op, op.fn_ubg.call())
        source = source.replace("    /* UBG PLACEHOLDER*/", ubg)

        mappers = cpp_optimizer_helper.build_mappers(op)
        source = source.replace("/* MAPPERS PLACEHOLDER*/", mappers)

        osstreams = cpp_optimizer_helper.build_osstreams(op)
        source = source.replace("/* OS STREAM PLACEHOLDER*/", osstreams)

        operators = cpp_optimizer_helper.build_operators(op)
        source = source.replace("/* OPERATORS PLACEHOLDER*/", operators)

        if path is None:
            file_path = './' + op.name + "_problem_ipopt.cpp"
        else:
            file_path = Path(path + '/' + op.name + "_problem_ipopt.cpp").expanduser()
        print(file_path)
        with open(file_path, "w") as f:
            f.write(source)

    def build_objective(self,op:OptimizationProblem):
        ret = scalar_expression_parser.parse_scalar_casadi_expression("obj_value", op.objective)
        ret = substitute_variables.substitute_variables(ret, op, True)
        return ret

    def build_initialization_objective_hessian(self, op: OptimizationProblem, H: casadi.SX) -> str:
        ret = dense_expression_parser.parse_dense_casadi_expression('H', H)
        ret = substitute_variables.substitute_variables(ret, op, True)
        return ret

    def build_initialization_objective_jacobian(self, op: OptimizationProblem, g: casadi.SX) -> str:
        ret = dense_expression_parser.parse_dense_casadi_expression('g', g, one_dimensional=True)
        ret = substitute_variables.substitute_variables(ret, op, True)
        return ret

    def build_objective_jacobian(self, op: OptimizationProblem) -> str:
        ret = dense_expression_parser.parse_dense_casadi_expression('grad_f', op.objective_jacobian.T, one_dimensional=True)
        ret = substitute_variables.substitute_variables(ret, op, True)
        return ret

    def build_objective_hessian(self, op: OptimizationProblem, H: casadi.SX) -> str:
        ret = dense_expression_parser.parse_dense_casadi_expression('H', H)
        ret = substitute_variables.substitute_variables(ret, op, True)
        return ret

    def build_linearized_constraints_without_offset(self, op: OptimizationProblem, A: casadi.SX) -> str:
        ret = dense_expression_parser.parse_dense_casadi_expression('A', A)
        ret = substitute_variables.substitute_variables(ret, op, True)
        return ret

    def build_linearized_constraints_offset(self, op: OptimizationProblem, bA_correction: casadi.SX) -> str:
        lbA = op.fn_lbg.call(op.problem_parameters, op.scenario_parameters)
        ret = dense_expression_parser.parse_dense_casadi_expression('lbA', lbA, True)

        ubA = op.fn_ubg.call(op.problem_parameters, op.scenario_parameters)
        ret += '\n' + dense_expression_parser.parse_dense_casadi_expression('ubA', ubA)
        ret = substitute_variables.substitute_variables(ret, op, True)
        return ret

    def build_constraints(self, op: OptimizationProblem, constraints: casadi.SX) -> str:
        ret = dense_expression_parser.parse_dense_casadi_expression('g', constraints, one_dimensional=True)
        ret = substitute_variables.substitute_variables(ret, op, True)
        return ret

    def build_sparse_constraint_jacobian(self, op: OptimizationProblem):
        constraint_jacobian = casadi.jacobian(op.constraints.equations_flat(), op.optvars.unpacked())
        idx = sparse_expression_parser.build_ipopt_index(constraint_jacobian)
        values = sparse_expression_parser.build_ipopt_values(constraint_jacobian)
        values = substitute_variables.substitute_variables(values, op, True)
        nnz = constraint_jacobian.nnz()
        return [idx, values, nnz]

    def build_sparse_lagrange_hessian(self, op:OptimizationProblem):
        is_lagrange_hessian_quadratic = math_helper.symetric_based_on_numeric(op.lagrangian_hessian, [op.optvars.unpacked(), op.problem_parameters.unpacked(), op.lambdas])
        nz = 0
        if is_lagrange_hessian_quadratic:
            for row in range(op.lagrangian_hessian.size(1)):
                for column in range(op.lagrangian_hessian.size(2)):
                    if column > row:
                        op.lagrangian_hessian[row, column] = 0
                    if str(op.lagrangian_hessian[row, column]) == '0' or str(op.lagrangian_hessian[row, column]) == '00':
                         nz += 1

        nnz = op.lagrangian_hessian.size(1) * op.lagrangian_hessian.size(2) - nz
        idx = sparse_expression_parser.build_ipopt_index(op.lagrangian_hessian, is_lagrange_hessian_quadratic)
        value = sparse_expression_parser.build_ipopt_values(op.lagrangian_hessian, is_lagrange_hessian_quadratic)
        value = substitute_variables.substitute_variables(value, op, True)
        return [idx, value, nnz]


    def build_constraint_derivatives(self, op: OptimizationProblem, dconstr: casadi.SX) -> str:
        ret = dense_expression_parser.parse_dense_casadi_expression('dconstraints', dconstr, False)
        ret = substitute_variables.substitute_variables(ret, op, True)
        return ret

    def build_parameters(self, op: OptimizationProblem, parameters: casadi.SX):
        ret = dense_expression_parser.parse_dense_casadi_expression('parameters', parameters)
        ret = substitute_variables.substitute_variables(ret, op, True)
        return ret

    def build_initial_guess(self, op: OptimizationProblem, initial_guess: casadi.SX, var_name='initial_guess'):
        ret = dense_expression_parser.parse_dense_casadi_expression(var_name, initial_guess, one_dimensional=True)
        ret = substitute_variables.substitute_variables(ret, op, True)
        return ret

    def build_lower_box_boundaries(self, op: OptimizationProblem, lbx: casadi.SX):
        ret = dense_expression_parser.parse_dense_casadi_expression('lbx', lbx, one_dimensional=True)
        ret = substitute_variables.substitute_variables(ret, op, True)
        return ret

    def build_upper_box_boundaries(self, op: OptimizationProblem, ubx: casadi.SX):
        ret = dense_expression_parser.parse_dense_casadi_expression('ubx', ubx, one_dimensional=True)
        ret = substitute_variables.substitute_variables(ret, op, True)
        return ret

    def build_lower_constraint_boundaries(self, op: OptimizationProblem, lbg: casadi.SX):
        ret = dense_expression_parser.parse_dense_casadi_expression('lbg', lbg, one_dimensional=True)
        ret = substitute_variables.substitute_variables(ret, op, True)
        return ret

    def build_upper_constraint_boundaries(self, op: OptimizationProblem, ubg: casadi.SX):
        ret = dense_expression_parser.parse_dense_casadi_expression('ubg', ubg, one_dimensional=True)
        ret = substitute_variables.substitute_variables(ret, op, True)
        return ret
