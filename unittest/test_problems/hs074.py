import casadi
import math

import os
modulepath = os.path.dirname(__file__)
import sys
sys.path.append(f"{modulepath}/../..")
from optimizationproblem import OptimizationProblem

def hs074_problem():
    ocp = OptimizationProblem()
    ocp.name = 'hs074'

    x = casadi.SX.sym("xi", 2, 2)
    ocp.optvars.register("xi", x)

    # objective = x[0]*x[3]*(x[0]+x[1]+x[2])+x[2]
    objective = x[0,0]*x[1,1]*(x[0,0]+x[1,0]+x[0,1])+x[0,1]
    ocp.register_objective(objective)

    c1 = x[0,0]*x[1,0]*x[0,1]*x[1,1]
    ocp.constraints.register("c1", c1)

    c2 = x[0,0]**2 + x[1,0]**2 + x[0,1]**2 + x[1,1]**2
    ocp.constraints.register("c2", c2)

    return ocp

def add_hs074_build_functions(ocp):
    init_guess = casadi.SX(ocp.optvars.n_vars, 1)
    X_guess = casadi.SX.sym("X_guess", 2, 2)
    ocp.scenario_parameters.register("X_guess", X_guess)
    init_guess[0] = X_guess[0, 0]
    init_guess[1] = X_guess[1, 0]
    init_guess[2] = X_guess[0, 1]
    init_guess[3] = X_guess[1, 1]
    ocp.register_initial_guess_function(init_guess)

    lbg = casadi.SX.sym("lbg", ocp.constraints.n_constraints)
    ubg = casadi.SX.sym("ubg", ocp.constraints.n_constraints)
    lbg[0] = 25
    lbg[1] = 40
    ubg[0] = math.inf
    ubg[1] = 40
    ocp.register_lower_inequality_constraint_limits_function(lbg)
    ocp.register_upper_inequality_constraint_limits_function(ubg)

    lbx = casadi.SX.sym("lbx", ocp.optvars.n_vars)
    ubx = casadi.SX.sym("ubx", ocp.optvars.n_vars)
    lbx[:] = 1
    ubx[:] = 5
    ocp.register_lower_box_limits_function(lbx)
    ocp.register_upper_box_limits_function(ubx)

    return ocp
