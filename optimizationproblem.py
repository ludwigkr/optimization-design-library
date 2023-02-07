#!/usr/bin/env python3
import casadi
import numpy as np

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
        self.constraints = Constraints()
        self.optvars = Variables()
        self.problem_parameter = Variables() # Variables passed to the solver, but which cannot be changed by it. E.g. plane orientation, etc..
        self.scenario_parameter = Variables() # Values required to build a specific optimization problem like current drone position, etc
        self.exported_defines = ExportedDefines()
        self.trajectory_parameter = ROSTrajectoryParameter()
        self.fn_initial_guess = Function()
        self.fn_params = Function()
        self.fn_lbx = Function()
        self.fn_ubx = Function()
        self.fn_lbg = Function()
        self.fn_ubg = Function()

    def register_objective(self, new_objective):
        self.objective = new_objective


    def rebuild_all_functions(self):
        self.fn_initial_guess.rebuild(self.problem_parameter, self.scenario_parameter)
        self.fn_lbx.rebuild(self.problem_parameter, self.scenario_parameter)
        self.fn_ubx.rebuild(self.problem_parameter, self.scenario_parameter)
        self.fn_lbg.rebuild(self.problem_parameter, self.scenario_parameter)
        self.fn_ubg.rebuild(self.problem_parameter, self.scenario_parameter)

    def register_initial_guess_function(self, initial_guess):
        self.fn_initial_guess.build("fn_initial_guess", self.problem_parameter, self.scenario_parameter, initial_guess)

    def register_lower_box_limits_function(self, lbx):
        self.fn_lbx.build("fn_lbx", self.problem_parameter, self.scenario_parameter, lbx)

    def register_upper_box_limits_function(self, ubx):
        self.fn_ubx.build("fn_ubx", self.problem_parameter, self.scenario_parameter, ubx)

    def register_lower_inequality_constraint_limits_function(self, lbg):
        self.fn_lbg.build("fn_lbg", self.problem_parameter, self.scenario_parameter, lbg)

    def register_upper_inequality_constraint_limits_function(self, ubg):
        self.fn_ubg.build("fn_ubg", self.problem_parameter, self.scenario_parameter, ubg)

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
        fn = casadi.Function("fn", [self.optvars.variables_flat(), self.problem_parameter.variables_flat()], [self.constraints.equations_flat()])
        if type(problem_parameters) == dict:
            problem_parameters = problem_parameters['flat']
        return fn(initial_guess, problem_parameters)
