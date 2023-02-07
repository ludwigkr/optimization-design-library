#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import numpy as np
import casadi
from casadi import SX, DM

sys.path.append("../")
sys.path.append("../optimization_design_library")
sys.path.append("../min_nlp")

from optimizationproblem import OptimizationProblem
import optimizationsolver
from helper import *
from ocp_min_nlp import optimization_problem_min_nlp

from optimizationconfiguration import load_optimizer_settings

def optimization_problem_min_nlp_with_params():
    ocp = optimization_problem_min_nlp()
    ocp.name = 'min_nlp_with_params'

    X = ocp.optvars.block_by_name('X')
    # Create Optimization Parameters
    P = SX.sym("P", 2, 1)
    ocp.problem_parameter.register('P', P)

    # Create constraints:
    constraint1 = X[0, 0] * X[1, 0] / P[0, 0]
    ocp.constraints.overwrite("c1", constraint1)
    constraint2 = X[0, 0]**2 + P[1, 0]
    ocp.constraints.overwrite("c2", constraint2)

    ocp.rebuild_all_functions()

    return ocp


if __name__ == "__main__":
    ocp = optimization_problem_min_nlp_with_params()

    # Build solver:
    opts = load_optimizer_settings("ipopt")
    solver = optimizationsolver.build_solver(ocp, opts)

    # Call solver for one scenario:
    scenario = ocp.scenario_parameter.unpacked([1, 1])
    problem_parameters = ocp.problem_parameter.unpacked([2, 1])
    result = optimizationsolver.run(solver, ocp, scenario, problem_parameters)

    # Check the result (for )
    error = np.linalg.norm(np.array(result['x']) - np.array([0, 0]))
    assert(error < 1e-2)

    # problem_parameters = ocp.problem_parameter.unpacked()
    optimizationsolver.write_formulation(ocp, scenario, problem_parameters, result)