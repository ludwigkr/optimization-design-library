#!/usr/bin/env python3
import os
import sys
import casadi
from pathlib import Path

local_folder_path = os.path.dirname(__file__)
sys.path.append(local_folder_path + "../")
from optimizationproblem import OptimizationProblem
from qpelements import QuadraticOptimizerElements
from problembuildhelper import ProblemBuildHelper
from math_helper import symetric_based_on_numeric

class IpoptBuilder:
    def __init__(self) -> None:
        self.problem_build_helper = ProblemBuildHelper()

    def build(self, op: OptimizationProblem, qoe: QuadraticOptimizerElements, path:str) -> None:
        self.builder_header(op, path)
        self.build_source(op, qoe, path)


    def builder_header(self, op: OptimizationProblem, path: str) -> None:
            with open(local_folder_path + '/problem_template.h', 'r') as f:
                header = f.read()

            n_xopts = op.optvars.n_vars
            n_constraints = op.constraints.n_constraints
            n_params = op.problem_parameters.n_vars
            class_name = self.problem_build_helper.class_name(op.name)
            header = header.replace("N_DIMS_H", str(n_xopts**2))
            header = header.replace("N_DIMS_A", str(n_xopts*n_constraints))
            header = header.replace("N_XOPTS", str(n_xopts))
            header = header.replace("N_PARAMS", str(n_params))
            header = header.replace("N_CONSTRAINTS", str(n_constraints))
            header = header.replace("Problem", class_name)
            header = header.replace("struct scenario_parameter;", self.problem_build_helper.variable_structure_definition("scenario_parameter", op.scenario_parameters))
            header = header.replace("struct problem_parameter;",  self.problem_build_helper.variable_structure_definition("problem_parameter", op.problem_parameters))
            header = header.replace("struct optimized_variable;",  self.problem_build_helper.variable_structure_definition("optimized_variable", op.optvars))

            if path is None:
                file_path = './' + op.name + "_problem_ipopt.h"
            else:
                file_path = Path(path + '/' + op.name + "_problem_ipopt.h").expanduser()
            print(file_path)
            with open(file_path, "w") as f:
                f.write(header)

    def build_source(self, op: OptimizationProblem, qoe: QuadraticOptimizerElements, path: str) -> None:
        n_constraints = op.constraints.n_constraints
        n_xopts = op.optvars.n_vars
        lagrange_hessian_quadratic = symetric_based_on_numeric(op.lagrangian_hessian, [op.optvars.unpacked(), op.problem_parameters.unpacked(), op.lambdas])
        lagrange_hessian_zeros = 0
        if lagrange_hessian_quadratic:
            for row in range(op.lagrangian_hessian.size(1)):
                for column in range(op.lagrangian_hessian.size(2)):
                    if column > row:
                        op.lagrangian_hessian[row, column] = 0
                    if str(op.lagrangian_hessian[row, column]) == '0':
                        lagrange_hessian_zeros += 1


        with open(local_folder_path + '/problem_template.cpp', 'r') as f:
            source = f.read();

        source = source.replace("solvertemplate", op.name +"_quad_opti_qpoases")
        class_name = self.problem_build_helper.class_name(op.name)

        source = source.replace("formulation", op.name)
        source = source.replace('#include "problem_index.h"', '#include "' + str(op.name) + '_index.h"')
        source = source.replace("Problem", class_name)
        source = source.replace("N_XOPTS + N_CONSTRAINTS", str(n_xopts + n_constraints))
        source = source.replace("N_XOPTS", str(n_xopts))
        source = source.replace("N_CONSTRAINTS", str(n_constraints))
        source = source.replace("N_PARAMS", str(op.problem_parameters.n_vars))

        lagrangian_hessian_nnz = op.lagrangian_hessian.size(1) * op.lagrangian_hessian.size(2) - lagrange_hessian_zeros
        source = source.replace("LAGRANGE_HESSIAN_NNZ", str(lagrangian_hessian_nnz))

        source = source.replace("/* OBJECTIVE PLACEHOLDER*/", self.problem_build_helper.build_scalar_for_optimizer_formulation(op, "obj_value", op.objective, prob_param_as_struct=True))
        source = source.replace("    /* OBJECTIVE_JACOBIAN PLACEHOLDER*/", self.problem_build_helper.build_vectormatrix_for_optimizer_formulation(op, "grad_f", op.objective_jacobian.T, as_vector=True, dense=True, prob_param_as_struct=True))

        constraint_jacobian = casadi.jacobian(op.constraints.equations_flat(), op.optvars.unpacked())
        source = source.replace("        /* CONSTRAINTS_JACOBIAN_SPARSE_INDEX PLACEHOLDER*/", self.problem_build_helper.build_ipopt_index(op, constraint_jacobian))
        source = source.replace("        /* CONSTRAINTS_JACOBIAN_SPARSE_VALUES PLACEHOLDER*/", self.problem_build_helper.build_ipopt_values(op, constraint_jacobian))
        constraint_jacobian_nnz = constraint_jacobian.nnz()
        source = source.replace("CONSTRAINTS_JACOBIAN_NNZ", str(constraint_jacobian_nnz))


        source = source.replace("        /* LAGRANGIAN_HESSIAN_SPARSE_INDEX PLACEHOLDER*/", self.problem_build_helper.build_ipopt_index(op, op.lagrangian_hessian, lagrange_hessian_quadratic))
        source = source.replace("        /* LAGRANGIAN_HESSIAN_SPARSE_VALUES PLACEHOLDER*/", self.problem_build_helper.build_ipopt_values(op, op.lagrangian_hessian, lagrange_hessian_quadratic))
        
        source = source.replace("    /*WRITE BACK SOLUTION PLACEHOLDER*/", self.problem_build_helper.build_struct_of_variable("xopt", op.optvars, pointer=True))

        init_H = self.build_initH(op, qoe.objective_hessian)
        source = source.replace("    /* INIT H PLACEHOLDER*/", init_H)

        update_H = self.build_updateH(op, qoe.objective_hessian)
        source = source.replace("    /* UPDATE H PLACEHOLDER*/", update_H)

        init_g = self.build_initg(op, qoe.objective_jacobian)
        source = source.replace("    /* INIT g PLACEHOLDER*/", init_g)

        update_g = self.build_updateg(op, qoe.objective_jacobian)
        source = source.replace("    /* UPDATE g PLACEHOLDER*/", update_g)

        A = self.build_A(op, qoe.constraints_jacobian)
        source = source.replace("    /* UPDATE A PLACEHOLDER*/", A)

        bA = self.build_bA(op, qoe.cx0minusdcx0)
        source = source.replace("    /* UPDATE bA PLACEHOLDER*/", bA)

        source = source.replace("    /* CONSTRAINTS PLACEHOLDER*/", self.problem_build_helper.build_vectormatrix_for_optimizer_formulation(op, "g", op.constraints.equations_flat(), as_vector=True, dense=True, prob_param_as_struct=True))

        H = self.build_updateH(op, qoe.objective_hessian)
        source = source.replace("    /* UPDATE H PLACEHOLDER*/", H)

        dconstr = self.build_constraint_derivatives(op, qoe.constraints_jacobian)
        source = source.replace("    /* CONSTRAINT_DERIVATIVES PLACEHOLDER*/", dconstr)

        parameters = self.build_parameters(op, op.problem_parameters.variables_flat())
        source = source.replace("    /* PARAMS PLACEHOLDER*/", parameters).replace("parameters", "parameter")

        initial_guess = self.build_initial_guess(op, op.fn_initial_guess.call(), "x")
        source = source.replace("    /* INITIAL_GUESS PLACEHOLDER*/", initial_guess)

        lbx = self.build_lbx(op, op.fn_lbx.call())
        source = source.replace("    /* LBX PLACEHOLDER*/", lbx)

        ubx = self.build_ubx(op, op.fn_ubx.call())
        source = source.replace("    /* UBX PLACEHOLDER*/", ubx)

        lbg = self.build_lbg(op, op.fn_lbg.call())
        source = source.replace("    /* LBG PLACEHOLDER*/", lbg)

        ubg = self.build_ubg(op, op.fn_ubg.call())
        source = source.replace("    /* UBG PLACEHOLDER*/", ubg)

        if path is None:
            file_path = './' + op.name + "_problem_ipopt.cpp"
        else:
            file_path = Path(path + '/' + op.name + "_problem_ipopt.cpp").expanduser()
        print(file_path)
        with open(file_path, "w") as f:
            f.write(source)



    def build_initH(self, op: OptimizationProblem, H: casadi.SX) -> str:
        ret = self.problem_build_helper.build_matrix('H', H)
        ret = self.problem_build_helper.subsitude_variables(ret, op).replace("prob_param", "param")
        return ret

    def build_updateH(self, op: OptimizationProblem, H: casadi.SX) -> str:
        ret = self.problem_build_helper.build_matrix('H', H)
        ret = self.problem_build_helper.subsitude_variables(ret, op).replace("prob_param", "param")
        return ret

    def build_initg(self, op: OptimizationProblem, g: casadi.SX) -> str:
        ret = self.problem_build_helper.build_matrix('g', g)
        ret = self.problem_build_helper.subsitude_variables(ret, op)
        return ret

    def build_updateg(self, op: OptimizationProblem, g: casadi.SX) -> str:
        ret = self.problem_build_helper.build_matrix('g', g)
        ret = self.problem_build_helper.subsitude_variables(ret, op).replace("prob_param", "param")
        return ret

    def build_A(self, op: OptimizationProblem, A: casadi.SX) -> str:
        ret = self.problem_build_helper.build_matrix('A', A)
        ret = self.problem_build_helper.subsitude_variables(ret, op).replace("prob_param", "param")
        return ret

    def build_bA(self, op: OptimizationProblem, bA_correction: casadi.SX) -> str:
        lbA = op.fn_lbg.call(op.problem_parameters, op.scenario_parameters)
        ret = self.problem_build_helper.build_matrix('lbA', lbA)

        ubA = op.fn_ubg.call(op.problem_parameters, op.scenario_parameters)
        ret += '\n' + self.problem_build_helper.build_matrix('ubA', ubA)
        ret = self.problem_build_helper.subsitude_variables(ret, op).replace("prob_param", "param")
        return ret

    def build_constraints(self, op: OptimizationProblem, constraints: casadi.SX) -> str:
        ret = self.problem_build_helper.build_matrix('constraints', constraints)
        ret = self.problem_build_helper.subsitude_variables(ret, op).replace("prob_param", "param")
        return ret

    def build_constraint_derivatives(self, op: OptimizationProblem, dconstr: casadi.SX) -> str:
        ret = self.problem_build_helper.build_matrix('dconstraints', dconstr, False)
        ret = self.problem_build_helper.subsitude_variables(ret, op).replace("prob_param", "param")
        return ret

    def build_parameters(self, op: OptimizationProblem, parameters: casadi.SX):
        ret = self.problem_build_helper.build_matrix('parameters', parameters)
        ret = self.problem_build_helper.subsitude_variables(ret, op, True)
        return ret

    def build_initial_guess(self, op: OptimizationProblem, initial_guess: casadi.SX, var_name='initial_guess'):
        ret = self.problem_build_helper.build_matrix(var_name, initial_guess)
        ret = self.problem_build_helper.subsitude_variables(ret, op)
        return ret

    def build_lbx(self, op: OptimizationProblem, lbx: casadi.SX):
        ret = self.problem_build_helper.build_matrix('lbx', lbx)
        ret = self.problem_build_helper.subsitude_variables(ret, op)
        return ret

    def build_ubx(self, op: OptimizationProblem, ubx: casadi.SX):
        ret = self.problem_build_helper.build_matrix('ubx', ubx)
        ret = self.problem_build_helper.subsitude_variables(ret, op)
        return ret

    def build_lbg(self, op: OptimizationProblem, lbg: casadi.SX):
        ret = self.problem_build_helper.build_matrix('lbg', lbg)
        ret = self.problem_build_helper.subsitude_variables(ret, op)
        return ret

    def build_ubg(self, op: OptimizationProblem, ubg: casadi.SX):
        ret = self.problem_build_helper.build_matrix('ubg', ubg)
        ret = self.problem_build_helper.subsitude_variables(ret, op)
        return ret
