import casadi
import math

import os
modulepath = os.path.dirname(__file__)
import sys
sys.path.append(f"{modulepath}/../..")
from optimizationproblem import OptimizationProblem

def nlopt_example_problem():
    ocp = OptimizationProblem()
    ocp.name = 'nlopt_example'

    x = ocp.optvars.register("xi_", 2)

    objective = casadi.sqrt(x[1])
    ocp.register_objective(objective)

    a = ocp.problem_parameters.register('aparam', 2)
    b = ocp.problem_parameters.register('bparam', 2)

    c1 = (a[0] * x[0] + b[0])**3 - x[1]
    ocp.constraints.register("c1", c1)

    c2 = casadi.power(a[1] * x[0] + b[1], 3) - x[1]
    ocp.constraints.register("c2", c2)

    return ocp

def add_nlopt_example_build_functions(ocp: OptimizationProblem):
    init_guess_var = ocp.scenario_parameters.register("init_guess", 2)
    xopt = ocp.optvars.variables_flat()
    init_guess = casadi.SX(ocp.optvars.n_vars, 1)
    init_guess[0] = init_guess_var[0]
    init_guess[1] = init_guess_var[1]
    ocp.register_initial_guess_function(init_guess)

    lbg = casadi.SX.sym("lbg", ocp.constraints.n_constraints)
    ubg = casadi.SX.sym("ubg", ocp.constraints.n_constraints)
    lbg[0] = -math.inf
    lbg[1] = -math.inf
    ubg[0] = 0
    ubg[1] = 0
    ocp.register_lower_inequality_constraint_limits_function(lbg)
    ocp.register_upper_inequality_constraint_limits_function(ubg)

    lbx = casadi.SX.sym("lbx", ocp.optvars.n_vars)
    ubx = casadi.SX.sym("ubx", ocp.optvars.n_vars)
    lbx[0] = -math.inf
    lbx[1] = 0
    ubx[:] = math.inf
    ocp.register_lower_box_limits_function(lbx)
    ocp.register_upper_box_limits_function(ubx)

    return ocp
