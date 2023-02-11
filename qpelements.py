#!/usr/bin/env python3
import casadi
from optimizationproblem import OptimizationProblem

class QuadraticOptimizerElements:
    def __init__(self, op:OptimizationProblem):
        optvars = op.optvars.variables_flat()
        params = op.problem_parameter.variables_flat()
        constraints = op.constraints.equations_flat()
        n_constr = op.constraints.n_constraints
        lam_g = casadi.SX.sym('lamg', n_constr, 1) # Langrange multiplier constraint equations

        self.objective_jacobian = casadi.jacobian(op.objective, optvars)
        self.constraints_jacobian = casadi.jacobian(constraints, optvars)
        self.objective_hessian = casadi.jacobian(self.objective_jacobian, optvars)

        for c in range(n_constr):
            self.objective_hessian += casadi.jacobian(lam_g[c] * self.constraints_jacobian[c,:], optvars)

        self.cx0minusdcx0 = constraints - self.constraints_jacobian@optvars
