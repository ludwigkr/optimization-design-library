#!/usr/bin/env python3
import os
import sys
import casadi

local_folder_path = os.path.dirname(__file__)
sys.path.append(local_folder_path + "../")
from optimizationproblem import OptimizationProblem
from qpelements import QuadraticOptimizerElements
from problembuildhelper import ProblemBuildHelper

class QpoasesBuilder:
    def __init__(self) -> None:
        self.problem_build_helper = ProblemBuildHelper()

    def build(self, op: OptimizationProblem, qoe: QuadraticOptimizerElements) -> None:
        self.builder_header(op)
        self.build_source(op, qoe)


    def builder_header(self, op: OptimizationProblem) -> None:
            with open(local_folder_path + '/solvertemplate_qpoases.h', 'r') as f:
                header = f.read()

            n_xopts = op.optvars.n_vars
            n_constraints = op.constraints.n_constraints
            class_name = self.problem_build_helper.class_name(op.name)
            header = header.replace("N_DIMS_H", str(n_xopts**2))
            header = header.replace("N_DIMS_A", str(n_xopts*n_constraints))
            header = header.replace("N_XOPTS", str(n_xopts))
            header = header.replace("N_CONSTRAINTS", str(n_constraints))
            header = header.replace("SolverTemplate", class_name)
            header = header.replace("struct scenario_parameter;", self.problem_build_helper.variable_structure_definition("scenario_parameter", op.scenario_parameter))
            header = header.replace("struct problem_parameter;",  self.problem_build_helper.variable_structure_definition("problem_parameter", op.problem_parameter))

            file_name = op.name + "_quad_opti_qpoases.h"
            print(file_name)
            with open('./' + file_name, "w") as f:
                f.write(header)

    def build_source(self, op: OptimizationProblem, qoe: QuadraticOptimizerElements) -> None:
        n_constraints = op.constraints.n_constraints 
        n_xopts = op.optvars.n_vars

        with open(local_folder_path + '/solvertemplate_qpoases.cpp', 'r') as f:
            source = f.read();

        source = source.replace("solvertemplate", op.name +"_quad_opti_qpoases")
        class_name = self.problem_build_helper.class_name(op.name)
        source = source.replace('#include "problem_index.h"', '#include "' + str(op.name) + '_index.h"')
        source = source.replace("SolverTemplate", class_name)
        source = source.replace("N_XOPTS + N_CONSTRAINTS", str(n_xopts + n_constraints))
        source = source.replace("N_XOPTS", str(n_xopts))
        source = source.replace("N_CONSTRAINTS", str(n_constraints))

        init_H = self.build_H(op, qoe.objective_hessian)
        source = source.replace("    /* INIT H PLACEHOLDER*/", init_H)
        init_g = self.build_initg(op, qoe.objective_jacobian)
        source = source.replace("    /* INIT g PLACEHOLDER*/", init_g)

        A = self.build_A(op, qoe.constraints_jacobian)
        source = source.replace("    /* UPDATE A PLACEHOLDER*/", A)

        bA = self.build_bA(op, qoe.cx0minusdcx0)
        source = source.replace("    /* UPDATE bA PLACEHOLDER*/", bA)

        c = self.build_constraints(op, op.constraints.equations_flat())
        source = source.replace("    /* CONSTRAINTS PLACEHOLDER*/", c)

        H = self.build_H(op, qoe.objective_hessian)
        source = source.replace("    /* UPDATE H PLACEHOLDER*/", H)

        dconstr = self.build_constraint_derivatives(op, qoe.constraints_jacobian)
        source = source.replace("    /* CONSTRAINT_DERIVATIVES PLACEHOLDER*/", dconstr)

        parameters = self.build_parameters(op, op.problem_parameter.variables_flat())
        # parameters = build_scenario_dependent_vector("parameters",
        # optimizer_text_elements["problem_parameter"],
        # optimizer_text_elements["scenario_parameter"],
        # optimizer_text_elements["parameter_builder_fn"])
        source = source.replace("    /* PARAMS PLACEHOLDER*/", parameters)

        initial_guess = self.build_initial_guess(op, op.fn_initial_guess.call())
        source = source.replace("    /* INITIAL_GUESS PLACEHOLDER*/", initial_guess)

        # lbx = build_scenario_dependent_vector("lbx",
        # optimizer_text_elements["problem_parameter"],
        # optimizer_text_elements["scenario_parameter"],
        # optimizer_text_elements["lbx"])
        # source = source.replace("    /* LBX PLACEHOLDER*/", lbx)

        # ubx = build_scenario_dependent_vector("ubx",
        # optimizer_text_elements["problem_parameter"],
        # optimizer_text_elements["scenario_parameter"],
        # optimizer_text_elements["ubx"])
        # source = source.replace("    /* UBX PLACEHOLDER*/", ubx)

        # lbg = build_scenario_dependent_vector("lbg",
        # optimizer_text_elements["problem_parameter"],
        # optimizer_text_elements["scenario_parameter"],
        # optimizer_text_elements["lbg"])
        # source = source.replace("    /* LBG PLACEHOLDER*/", lbg)

        # ubg = build_scenario_dependent_vector("ubg",
        # optimizer_text_elements["problem_parameter"],
        # optimizer_text_elements["scenario_parameter"],
        # optimizer_text_elements["ubg"])
        # source = source.replace("    /* UBG PLACEHOLDER*/", ubg)

        file_name = op.name + "_quad_opti_qpoases.cpp"
        print(file_name)
        with open('./' + file_name, "w") as f:
            f.write(source)
 
    def subsitude_variables(self, exp: str, op: OptimizationProblem) -> str:
        ret = self.problem_build_helper.substitude_variable(exp, 'X', 'xopt', op.optvars.n_vars)
        ret = self.problem_build_helper.substitude_variable(ret, 'lamg', 'lamg', op.constraints.n_constraints)
        ret = self.problem_build_helper.substitute_variable(ret, 'prob_params', '->', op.problem_parameter)
        ret = self.problem_build_helper.substitute_variable(ret, 'scenario', '->', op.scenario_parameter)
        return ret


    def build_H(self, op: OptimizationProblem, H: casadi.SX) -> str:
        ret = self.problem_build_helper.build_dense_matrix('H', H)
        ret = self.subsitude_variables(ret, op)
        return ret

    def build_initg(self, op: OptimizationProblem, g: casadi.SX) -> str:
        ret = self.problem_build_helper.build_dense_matrix('g', g)
        ret = self.subsitude_variables(ret, op)
        return ret

    def build_A(self, op: OptimizationProblem, A: casadi.SX) -> str:
        ret = self.problem_build_helper.build_dense_matrix('A', A)
        ret = self.subsitude_variables(ret, op)
        return ret

    def build_bA(self, op: OptimizationProblem, bA_correction: casadi.SX) -> str:
        lbA = op.fn_lbg.call(op.problem_parameter, op.scenario_parameter)
        ret = self.problem_build_helper.build_dense_matrix('lbA', lbA)

        ubA = op.fn_ubg.call(op.problem_parameter, op.scenario_parameter)
        ret += '\n' + self.problem_build_helper.build_dense_matrix('ubA', ubA)
        ret = self.subsitude_variables(ret, op)
        return ret

    def build_constraints(self, op: OptimizationProblem, constraints: casadi.SX) -> str:
        ret = self.problem_build_helper.build_dense_matrix('constraints', constraints)
        ret = self.subsitude_variables(ret, op)
        return ret


    def build_constraint_derivatives(self, op: OptimizationProblem, dconstr: casadi.SX) -> str:
        ret = self.problem_build_helper.build_dense_matrix('dconstraints', dconstr)
        ret = self.subsitude_variables(ret, op)
        return ret

    def build_parameters(self, op: OptimizationProblem, parameters: casadi.SX):
        ret = self.problem_build_helper.build_dense_matrix('parameters', parameters)
        ret = self.subsitude_variables(ret, op)
        return ret

    def build_initial_guess(self, op: OptimizationProblem, initial_guess: casadi.SX):
        ret = self.problem_build_helper.build_dense_matrix('initial_guess', initial_guess)
        ret = self.subsitude_variables(ret, op)
        return ret