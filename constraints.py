#!/usr/bin/env python3
import casadi
import numpy as np

class Constraints:
    def __init__(self):
        self.n_constraints = 0
        self.idxs = {}
        self.equations = []

    def __update_constraint_index(self, new_constraints):
        """Based on the new constraints, updates the total amount of constraints n_ineq and saves the indices of the constraints in ineq_idxs."""
        n_new_constraints = new_constraints.shape[0]
        ineq_idxs = np.linspace(self.n_constraints, self.n_constraints + n_new_constraints - 1, n_new_constraints, dtype=int)
        self.n_constraints += n_new_constraints

        return ineq_idxs

    def register(self, name, new_constraints):
        assert(type(new_constraints) == casadi.casadi.SX)
        assert(type(name)== str)
        new_constraints = casadi.reshape(new_constraints, -1, 1)
        self.idxs[name] = self.__update_constraint_index(new_constraints)
        self.equations.append(new_constraints)

    def overwrite(self, name, new_constraints):
        assert(type(new_constraints) == casadi.casadi.SX)
        assert(type(name)== str)
        assert (name in self.idxs)
        new_constraints = casadi.reshape(new_constraints, -1, 1)
        assert(len(self.idxs[name]) == new_constraints.size1())
        j = 0
        for i in self.idxs[name]:
            self.equations[i] = new_constraints[j]
            j += 1

    def equations_flat(self):
        ocp_constraints = []
        for i in range(len(self.equations)):
            ocp_constraints = casadi.vertcat(ocp_constraints, self.equations[i])
        return ocp_constraints
