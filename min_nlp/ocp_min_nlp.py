#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import numpy as np
import casadi
from casadi import SX, DM

sys.path.append("../")
sys.path.append("../optimization_design_library")

from optimizationproblem import OptimizationProblem
import optimizationsolver
from build_cpp import CppBuilder
from optimizationconfiguration import load_optimizer_settings

def optimization_problem_min_nlp():
    # Initialize the optmization problem
    ocp = OptimizationProblem()
    ocp.name = 'min_nlp'

    # Create Optimization Variables
    X = SX.sym('X', 2, 1)
    ocp.optvars.register('X', X)

    # Create Objective
    objective = casadi.sum1(casadi.sum2(X[:, :]**2))
    ocp.register_objective(objective)

    # Create constraints:
    constraint1 = X[0, 0] * X[1, 0]
    ocp.constraints.register("c1", constraint1)
    constraint2 = X[0, 0]**2
    ocp.constraints.register("c2", constraint2)

    # Create scenario parameter:
    SP = SX.sym('SP', ocp.optvars.n_vars, 1)
    ocp.scenario_parameter.register("SP", SP)

    # Create initial guess:
    X0 = SX.sym('X0', ocp.optvars.n_vars, 1)
    X0[0] = SP[0]
    X0[1] = SP[0] + SP[1]
    ocp.register_initial_guess_function(X0)

    # Set box constraint limits
    ocp.register_lower_box_limits_function([-1, -1])
    ocp.register_upper_box_limits_function([2, 2])

    # Set inequality constraint limits:
    ocp.register_lower_inequality_constraint_limits_function([0, 0])
    ocp.register_upper_inequality_constraint_limits_function([0, 0])

    return ocp


if __name__ == "__main__":
    ocp = optimization_problem_min_nlp()

    # Build solver:
    opts = load_optimizer_settings()
    solver = optimizationsolver.build_solver(ocp, opts)

    # Call solver for one scenario:
    scenario = ocp.scenario_parameter.packed([1, 1])
    result = optimizationsolver.run(solver, ocp, scenario)

    # Check the result (for )
    error = np.linalg.norm(np.array(result['x']) - np.array([0, 0]))
    assert(error < 1e-5)

    problem_parameters = ocp.problem_parameter.unpacked()
    optimizationsolver.write_formulation(ocp, scenario, problem_parameters, result)

    cppbuilder = CppBuilder()
    cppbuilder.build(ocp)