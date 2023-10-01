#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import numpy as np
from casadi import SX

sys.path.append("../")
sys.path.append("../optimization_design_library")
sys.path.append("../min_nlp")

from optimizationproblem import OptimizationProblem
import optimizationsolver
from build_cpp import CppBuilder
from ocp_min_nlp import optimization_problem_min_nlp

from optimizationconfiguration import load_optimizer_settings

def optimization_problem_min_nlp_with_params():
    ocp = optimization_problem_min_nlp()
    ocp.name = 'min_nlp_with_params'

    X = ocp.optvars.block_by_name('X')
    # Create Optimization Parameters
    P = SX.sym("P", 1, 1)
    ocp.problem_parameters.register('P', P)

    # Create constraints:
    constraint1 = X[1,:] - P[0, 0] * X[0,:]
    ocp.constraints.overwrite("c1", constraint1)

    ocp.rebuild_all_functions()

    return ocp


if __name__ == "__main__":
    ocp = optimization_problem_min_nlp_with_params()

    # Build solver:
    opts = load_optimizer_settings("ipopt")
    solver = optimizationsolver.build_solver(ocp, opts)

    # Call solver for one scenario:
    scenario = ocp.scenario_parameters.packed([10, 10])
    problem_parameters = ocp.problem_parameters.unpacked([1])

    result = optimizationsolver.run(solver, ocp, scenario, problem_parameters)

    # Check the result (for )
    error = np.linalg.norm(np.array(result['x']) - np.array([[2.5, 4.5]]).T)
    assert(error < 1e-5)

    # Check if parameters is actually changing the result:
    problem_parameters = ocp.problem_parameters.unpacked([2])
    result = optimizationsolver.run(solver, ocp, scenario, problem_parameters)
    error = np.linalg.norm(np.array(result['x']) - np.array([[2.5, 4.5]]).T)
    assert(error > 1e-5) # Error should be different

    # problem_parameters = ocp.problem_parameters.unpacked()
    optimizationsolver.write_formulation(ocp, scenario, problem_parameters, result)

    case_exporter = optimizationsolver.TestCaseExporter()
    case_exporter.add_case(ocp, scenario, problem_parameters, result)
    case_exporter.save("./tests_min_nlp_with_params.json")

    cppbuilder = CppBuilder()
    cppbuilder.build(ocp)
