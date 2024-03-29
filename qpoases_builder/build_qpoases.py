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

class QpoasesBuilder:
    def __init__(self) -> None:
        self.problem_build_helper = ProblemBuildHelper()

    def build(self, op: OptimizationProblem, qoe: QuadraticOptimizerElements, path:str) -> None:
        self.builder_header(op, path)
        self.build_source(op, qoe, path)


    def builder_header(self, op: OptimizationProblem, path: str) -> None:
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
            header = header.replace("struct scenario_parameter;", self.problem_build_helper.variable_structure_definition("scenario_parameter", op.scenario_parameters))
            header = header.replace("struct problem_parameter;",  self.problem_build_helper.variable_structure_definition("problem_parameter", op.problem_parameters))

            if path is None:
                file_path = './' + op.name + "_quad_opti_qpoases.h"
            else:
                file_path = Path(path + '/' + op.name + "_quad_opti_qpoases.h").expanduser()
            print(file_path)
            with open(file_path, "w") as f:
                f.write(header)

    def build_source(self, op: OptimizationProblem, qoe: QuadraticOptimizerElements, path: str) -> None:
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
        source = source.replace("N_PARAMS", str(op.problem_parameters.n_vars))

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

        c = self.build_constraints(op, op.constraints.equations_flat())
        source = source.replace("    /* CONSTRAINTS PLACEHOLDER*/", c)

        H = self.build_updateH(op, qoe.objective_hessian)
        source = source.replace("    /* UPDATE H PLACEHOLDER*/", H)

        dconstr = self.build_constraint_derivatives(op, qoe.constraints_jacobian)
        source = source.replace("    /* CONSTRAINT_DERIVATIVES PLACEHOLDER*/", dconstr)

        parameters = self.build_parameters(op, op.problem_parameters.variables_flat())
        source = source.replace("    /* PARAMS PLACEHOLDER*/", parameters)

        initial_guess = self.build_initial_guess(op, op.fn_initial_guess.call())
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
            file_path = './' + op.name + "_quad_opti_qpoases.cpp"
        else:
            file_path = Path(path + '/' + op.name + "_quad_opti_qpoases.cpp").expanduser()
        print(file_path)
        with open(file_path, "w") as f:
            f.write(source)

    def subsitude_variables(self, exp: str, op: OptimizationProblem, prob_param_as_struct=False) -> str:

        ret = exp
        for optvar_name in op.optvars.names:
            ret = self.problem_build_helper.substitude_variable(ret, optvar_name, 'xopt', op.optvars.idxs[optvar_name].size, op.optvars.idxs[optvar_name][0,0])

        if prob_param_as_struct:
            ret = self.problem_build_helper.substitute_variable_in_struct(ret, "prob_param", "->", op.problem_parameters)
        else:
            for param_name in op.problem_parameters.names:
                ret = self.problem_build_helper.substitude_variable(ret, param_name, 'param', op.problem_parameters.idxs[param_name].size, op.problem_parameters.idxs[param_name][0,0])

        ret = self.problem_build_helper.substitude_variable(ret, 'lamg', 'lamg', op.constraints.n_constraints)
        ret = self.problem_build_helper.substitute_variable_in_struct(ret, 'scenario', '->', op.scenario_parameters)
        return ret


    def build_initH(self, op: OptimizationProblem, H: casadi.SX) -> str:
        ret = self.problem_build_helper.build_dense_matrix('H', H)
        ret = self.subsitude_variables(ret, op).replace("prob_param", "param")
        return ret

    def build_updateH(self, op: OptimizationProblem, H: casadi.SX) -> str:
        ret = self.problem_build_helper.build_dense_matrix('H', H)
        ret = self.subsitude_variables(ret, op).replace("prob_param", "param")
        return ret

    def build_initg(self, op: OptimizationProblem, g: casadi.SX) -> str:
        ret = self.problem_build_helper.build_dense_matrix('g', g)
        ret = self.subsitude_variables(ret, op)
        return ret

    def build_updateg(self, op: OptimizationProblem, g: casadi.SX) -> str:
        ret = self.problem_build_helper.build_dense_matrix('g', g)
        ret = self.subsitude_variables(ret, op).replace("prob_param", "param")
        return ret

    def build_A(self, op: OptimizationProblem, A: casadi.SX) -> str:
        ret = self.problem_build_helper.build_dense_matrix('A', A)
        ret = self.subsitude_variables(ret, op).replace("prob_param", "param")
        return ret

    def build_bA(self, op: OptimizationProblem, bA_correction: casadi.SX) -> str:
        lbA = op.fn_lbg.call(op.problem_parameters, op.scenario_parameters)
        ret = self.problem_build_helper.build_dense_matrix('lbA', lbA)

        ubA = op.fn_ubg.call(op.problem_parameters, op.scenario_parameters)
        ret += '\n' + self.problem_build_helper.build_dense_matrix('ubA', ubA)
        ret = self.subsitude_variables(ret, op).replace("prob_param", "param")
        return ret

    def build_constraints(self, op: OptimizationProblem, constraints: casadi.SX) -> str:
        ret = self.problem_build_helper.build_dense_matrix('constraints', constraints)
        ret = self.subsitude_variables(ret, op).replace("prob_param", "param")
        return ret

    def build_constraint_derivatives(self, op: OptimizationProblem, dconstr: casadi.SX) -> str:
        ret = self.problem_build_helper.build_dense_matrix('dconstraints', dconstr, False)
        ret = self.subsitude_variables(ret, op).replace("prob_param", "param")
        return ret

    def build_parameters(self, op: OptimizationProblem, parameters: casadi.SX):
        ret = self.problem_build_helper.build_dense_matrix('parameters', parameters)
        ret = self.subsitude_variables(ret, op, True)
        return ret

    def build_initial_guess(self, op: OptimizationProblem, initial_guess: casadi.SX):
        ret = self.problem_build_helper.build_dense_matrix('initial_guess', initial_guess)
        ret = self.subsitude_variables(ret, op)
        return ret

    def build_lbx(self, op: OptimizationProblem, lbx: casadi.SX):
        ret = self.problem_build_helper.build_dense_matrix('lbx', lbx)
        ret = self.subsitude_variables(ret, op)
        return ret

    def build_ubx(self, op: OptimizationProblem, ubx: casadi.SX):
        ret = self.problem_build_helper.build_dense_matrix('ubx', ubx)
        ret = self.subsitude_variables(ret, op)
        return ret

    def build_lbg(self, op: OptimizationProblem, lbg: casadi.SX):
        ret = self.problem_build_helper.build_dense_matrix('lbg', lbg)
        ret = self.subsitude_variables(ret, op)
        return ret

    def build_ubg(self, op: OptimizationProblem, ubg: casadi.SX):
        ret = self.problem_build_helper.build_dense_matrix('ubg', ubg)
        ret = self.subsitude_variables(ret, op)
        return ret
