#!/usr/bin/env python3
import casadi
import numpy as np
from casadi import SX, DM

from variables import Variables
from function import Function
from constraints import Constraints

class ExportedDefines:
    def __init__(self):
        self.defines = {}
        self.code = ""

    def register_define(self, name, value):
        self.defines[name] = value
        self.code += "#define " + name.upper() + " " + str(value) + "\n"

class ROSTrajectoryParameter:
    """Parameters to plot parts of the optimization variable as trajectories in ROS"""
    def __init__(self):
        self.parameter = {}

    def register_trajectory(self, name, idx):
        self.parameter[name] = idx

class OptimizationProblem:
    def __init__(self):
        self.name = "optization_problem"
        self.version = "1.0.0"
        self.objective = None
        self.objective_jacobian = None
        self.objective_hessian = None
        self.constraints = Constraints()
        self.optvars = Variables()
        self.problem_parameters = Variables() # Variables passed to the solver, but which cannot be changed by it. E.g. plane orientation, etc..
        self.scenario_parameters = Variables() # Values required to build a specific optimization problem like current drone position, etc
        self.exported_defines = ExportedDefines()
        self.trajectory_parameters = ROSTrajectoryParameter()
        self.fn_initial_guess = Function()
        self.fn_params = Function()
        self.fn_lbx = Function()
        self.fn_ubx = Function()
        self.fn_lbg = Function()
        self.fn_ubg = Function()
        self.lambdas = None
        self.lagrangian = None
        self.lagrangian_jacobian = None
        self.lagrangian_hessian = None

    def register_objective(self, new_objective):
        self.objective = new_objective
        self.objective_jacobian = casadi.jacobian(new_objective, self.optvars.variables_flat())
        self.objective_hessian = casadi.jacobian(self.objective_jacobian, self.optvars.variables_flat())

    def rebuild_all_functions(self):
        self.fn_initial_guess.rebuild(self.problem_parameters, self.scenario_parameters)
        self.fn_lbx.rebuild(self.problem_parameters, self.scenario_parameters)
        self.fn_ubx.rebuild(self.problem_parameters, self.scenario_parameters)
        self.fn_lbg.rebuild(self.problem_parameters, self.scenario_parameters)
        self.fn_ubg.rebuild(self.problem_parameters, self.scenario_parameters)

    def register_initial_guess_function(self, initial_guess):
        self.fn_initial_guess.build("fn_initial_guess", self.problem_parameters, self.scenario_parameters, initial_guess)

    def register_lower_box_limits_function(self, lbx):
        self.fn_lbx.build("fn_lbx", self.problem_parameters, self.scenario_parameters, lbx)

    def register_upper_box_limits_function(self, ubx):
        self.fn_ubx.build("fn_ubx", self.problem_parameters, self.scenario_parameters, ubx)

    def register_lower_inequality_constraint_limits_function(self, lbg):
        self.fn_lbg.build("fn_lbg", self.problem_parameters, self.scenario_parameters, lbg)

    def register_upper_inequality_constraint_limits_function(self, ubg):
        self.fn_ubg.build("fn_ubg", self.problem_parameters, self.scenario_parameters, ubg)

    def absolute_constraints(self, V, E):
        """
        V is the variable which can be positive and negative.
        E is the variable wich only can be positive.
        """
        assert(V.size() == E.size())
        constraints = casadi.SX.zeros(V.size1(), 2 * V.size2())
        for i in range(E.size1()):
            for j in range(E.size2()):
                constraints[i, j]             = E[i,j] - V[i,j]
                constraints[i, j + E.size2()] = E[i,j] + V[i,j]
        return constraints

    def equation_values(self, initial_guess, problem_parameters):
        fn = casadi.Function("fn", [self.optvars.variables_flat(), self.problem_parameters.variables_flat()], [self.constraints.equations_flat()])
        if type(problem_parameters) == dict:
            problem_parameters = problem_parameters['flat']
        return fn(initial_guess, problem_parameters)

    def build_lagrangian(self):
        self.lagrangian = self.objective
        self.lambdas = SX.sym("lamg", self.constraints.n_constraints, 1)
        for i in range(self.constraints.n_constraints):
            self.lagrangian += self.lambdas[i] * self.constraints.equations_flat()[i]

        self.lagrangian_jacobian = casadi.jacobian(self.lagrangian, self.optvars.variables_flat())
        self.lagrangian_hessian = casadi.jacobian(self.lagrangian_jacobian, self.optvars.variables_flat())
