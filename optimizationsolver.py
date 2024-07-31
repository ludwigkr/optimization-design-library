from optimizationproblem import OptimizationProblem, Variables

import json
import os
import sys
import casadi
import numpy as np
from pathlib import Path

local_folder_path = os.path.dirname(__file__)
sys.path.append(local_folder_path + "/casadi_parser")

def build_solver(op: OptimizationProblem, opts):
    forbidden_variables = ['lam', 'x', 'xopt', 'param']

    assert(op.objective is not None)
    assert(not op.fn_initial_guess.function.is_null())
    assert(not op.fn_lbx.function.is_null())
    assert(not op.fn_ubx.function.is_null())
    assert(not op.fn_lbg.function.is_null())
    assert(not op.fn_ubg.function.is_null())
    for scenario in op.scenario_parameters.names:
        assert scenario not in forbidden_variables, f"{scenario} in {forbidden_variables =}, please change your variable name."

    for prob_param in op.problem_parameters.names:
        assert prob_param not in forbidden_variables, f"{prob_param} in {forbidden_variables =}, please change your variable name."

    for xopt in op.optvars.names:
        assert xopt not in forbidden_variables, f"{xopt} in {forbidden_variables =}, please change your variable name."

    op.fn_params.build('fn_problem_parameters', op.problem_parameters, op.scenario_parameters, op.problem_parameters.variables_flat())
    # assert(not op.fn_initial_guess.is_null())

    solver = casadi.nlpsol('solver', opts["optimizer"], {'x': op.optvars.variables_flat(), 'p': op.problem_parameters.variables_flat(), 'f': op.objective, 'g': op.constraints.equations_flat()}, opts["options"])
    # solver.generate_dependencies(op.name + '_optimizer.cpp', {'with_header': True, 'cpp': True})
    # os.system("gcc -fPIC -shared -O3 " + op.name + "_optimizer.cpp -o " + op.name + "_optimizer.so")
    # definition_export(op, op.exported_defines.code)

    return solver

def run(solver, op: OptimizationProblem, scenario_parameters: Variables, parameters: Variables=None):
    initial_guess = op.fn_initial_guess.call(parameters, scenario_parameters)
    lb = op.fn_lbx.call(parameters, scenario_parameters)
    ub = op.fn_ubx.call(parameters, scenario_parameters)
    lbg = op.fn_lbg.call(parameters, scenario_parameters)
    ubg = op.fn_ubg.call(parameters, scenario_parameters)

    if parameters is not None:
        result = solver(x0=initial_guess, p=parameters, lbg=lbg, ubg=ubg, lbx=lb, ubx=ub)
    else:
        result = solver(x0=initial_guess, lbg=lbg, ubg=ubg, lbx=lb, ubx=ub)

    return result
