#!/usr/bin/env python3

import os
import sys
import math
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

class NloptBuilder:
    def __init__(self):
        self.classname = None
        pass

    def build(self, op: OptimizationProblem, path:str) -> None:
        op.build_lagrangian()
        qoe = QuadraticOptimizerElements(op)
        self.classname = path_manager.class_name(op.name) + 'Problem'

        if not os.path.exists(path):
            os.mkdir(path)

        self.build_interface_header(op, path)
        self.build_interface_source(op, path)
        self.build_formulation_header(op, path)
        self.build_formulation_source(op, qoe, path)


    def build_interface_header(self, op: OptimizationProblem, path: str) -> None:
        with open(str(local_folder_path) + '/problem_interface.hpp', 'r') as f:
            header = f.read()

        header = header.replace('nxopts', str(op.optvars.n_vars))
        header = header.replace('problem_formulation', op.name + '_formulation')
        header = header.replace('Problem', self.classname)

        if path is None:
            file_path = './' + op.name + "_interface.hpp"
        else:
            file_path = Path(path + '/' + op.name + "_interface.hpp").expanduser()

        print(file_path)
        with open(file_path, "w") as f:
            f.write(header)


    def build_interface_source(self, op: OptimizationProblem, path: str):
        with open(str(local_folder_path) + '/problem_interface.cpp', 'r') as f:
            source = f.read()

        source = source.replace('problem_formulation', op.name + '_formulation')
        source = source.replace('nlopt_problem_interface', op.name + '_interface')
        source = source.replace('Problem', self.classname)

        if path is None:
            file_path = './' + op.name + "_interface.cpp"
        else:
            file_path = Path(path + '/' + op.name + "_interface.cpp").expanduser()

        print(file_path)
        with open(file_path, "w") as f:
            f.write(source)

    def build_formulation_header(self, op: OptimizationProblem, path: str) -> None:
        with open(str(local_folder_path) + '/problem_formulation.hpp', 'r') as f:
            header = f.read()

        header = header.replace("struct scenario_parameter;", cpp_struct_definition.cpp_struct_definition("scenario_parameter", op.scenario_parameters))
        header = header.replace("struct problem_parameter;", cpp_struct_definition.cpp_struct_definition("problem_parameter", op.problem_parameters))
        header = header.replace("struct optimized_variable;", cpp_struct_definition.cpp_struct_definition("optimized_variable", op.optvars))

        if path is None:
            file_path = './' + op.name + "_formulation.hpp"
        else:
            file_path = Path(path + '/' + op.name + "_formulation.hpp").expanduser()

        print(file_path)
        with open(file_path, "w") as f:
            f.write(header)


    def build_formulation_source(self, op: OptimizationProblem, qoe: QuadraticOptimizerElements, path: str) -> None:
        with open(str(local_folder_path) + '/problem_formulation.cpp', 'r') as f:
            source = f.read()

        source = source.replace('problem_formulation', op.name + '_formulation')

        objective = self.build_objective(op)
        source = source.replace("/* OBJECTIVE PLACEHOLDER*/",  objective)

        objective_jacobian = self.build_objective_jacobian(op)
        source = source.replace("    /* OBJECTIVE_JACOBIAN PLACEHOLDER*/", objective_jacobian)

        g = self.build_constraints(op)
        source = source.replace("    /* CONSTRAINTS PLACEHOLDER*/", g)

        dconstr = self.build_constraint_derivatives(op)
        source = source.replace("    /* CONSTRAINTS_JACOBIAN PLACEHOLDER*/", dconstr)

        initial_guess = self.build_initial_guess(op)
        source = source.replace("    /* INITIAL_GUESS PLACEHOLDER*/", initial_guess)

        lbx = self.build_lower_box_boundaries(op)
        source = source.replace("    /* LBX PLACEHOLDER*/", lbx)

        ubx = self.build_upper_box_boundaries(op)
        source = source.replace("    /* UBX PLACEHOLDER*/", ubx)

        xopt_result = self.build_xopt_result(op)
        source = source.replace("/* OPTIMIZED_VARIABLE PLACEHOLDER*/", xopt_result)

        osstreams = cpp_optimizer_helper.build_osstreams(op)
        source = source.replace("/* OS STREAM PLACEHOLDER*/", osstreams)

        if path is None:
            file_path = './' + op.name + "_formulation.cpp"
        else:
            file_path = Path(path + '/' + op.name + "_formulation.cpp").expanduser()

        print(file_path)
        with open(file_path, "w") as f:
            f.write(source)


    def build_objective(self, op: OptimizationProblem) -> str:
        ret = scalar_expression_parser.parse_scalar_casadi_expression("obj_value", op.objective)
        ret = substitute_variables.substitute_variables(ret, op, True)
        ret = ret.replace('xopt', 'x')
        return ret


    def build_objective_jacobian(self, op: OptimizationProblem) -> str:
        ret = dense_expression_parser.parse_dense_casadi_expression('grad', op.objective_jacobian, one_dimensional=True)
        ret = substitute_variables.substitute_variables(ret, op, True)
        ret = ret.replace('xopt', 'x')
        return ret

    def build_nlopt_constraints(self, op: OptimizationProblem) -> casadi.SX:
        constraints = op.constraints.equations_flat()
        lb = op.fn_lbg.call()
        ub = op.fn_ubg.call()

        # lb <= f(x) <= ub
        # f(x) <= 0
        nlopt_constraints = casadi.SX.sym("nlopt_constraints", (0, 1))
        for i in range(lb.size()[0]):
            if lb[i].is_symbolic() or not math.isinf(lb[i]):
                ci = lb[i] - constraints[i]
                nlopt_constraints = casadi.vertcat(nlopt_constraints, ci)

        for i in range(ub.size()[0]):
            if ub[i].is_symbolic() or not math.isinf(ub[i]):
                ci = constraints[i] - ub[i]
                nlopt_constraints = casadi.vertcat(nlopt_constraints, ci)

        return nlopt_constraints

    def build_constraints(self, op: OptimizationProblem) -> str:
        nlopt_constraints = self.build_nlopt_constraints(op)
        print(f"{nlopt_constraints = }")

        ret = dense_expression_parser.parse_dense_casadi_expression('result', nlopt_constraints, one_dimensional=True)
        ret = substitute_variables.substitute_variables(ret, op, True)
        ret = ret.replace('xopt', 'x')
        return ret


    def build_constraint_derivatives(self, op: OptimizationProblem):
        nlopt_constraints = self.build_nlopt_constraints(op)

        optvars = op.optvars.variables_flat()
        dnlopt_constraints = casadi.jacobian(nlopt_constraints, optvars)
        print(dnlopt_constraints)

        ret = dense_expression_parser.parse_dense_casadi_expression('grad', dnlopt_constraints, one_dimensional=True)
        ret = substitute_variables.substitute_variables(ret, op, True)
        ret = ret.replace('xopt', 'x')
        return ret


    def build_initial_guess(self, op: OptimizationProblem):
        init_guess = op.fn_initial_guess.call()

        ret = dense_expression_parser.parse_dense_casadi_expression('result', init_guess, one_dimensional=True)
        ret = substitute_variables.substitute_variables(ret, op, True)
        ret = ret.replace('xopt', 'x')

        return ret

    def build_lower_box_boundaries(self, op: OptimizationProblem):
        lb = op.fn_lbx.call()

        ret = dense_expression_parser.parse_dense_casadi_expression('result', lb, one_dimensional=True)
        ret = substitute_variables.substitute_variables(ret, op, True)
        ret = ret.replace('xopt', 'x')
        ret = ret.replace('inf', 'HUGE_VAL')

        return ret

    def build_upper_box_boundaries(self, op: OptimizationProblem):
        ub = op.fn_ubx.call()

        ret = dense_expression_parser.parse_dense_casadi_expression('result', ub, one_dimensional=True)
        ret = substitute_variables.substitute_variables(ret, op, True)
        ret = ret.replace('xopt', 'x')
        ret = ret.replace('inf', 'HUGE_VAL')

        return ret

    def build_xopt_result(self, op: OptimizationProblem):
        xopt_flat = op.optvars.variables_flat()
        xopt = op.optvars.pack_variables_fn()
        ret = ""
        
        for xopti_name in op.optvars.names:
            xopti_idx = op.optvars.idxs[xopti_name]
            if len(xopti_idx) == 1:
                ret += f"xopt->{xopti_name} = x[{xopti_idx[0][0]}];\n"
            else:
                xopti_idx = xopti_idx.T.reshape([-1]).tolist()
                values = [f'x[{idx}]' for idx in xopti_idx]
                values = ",".join(values)
                ret += f"xopt->{xopti_name} << {values};\n"

        return ret
