#!/usr/bin/env python3
import casadi
import numpy as np

from variables import Variables


class Function:
    def __init__(self):
        self.name = "func"
        self.function = casadi.Function()
        self.symbolic_output = casadi.SX()
        self.sym_problem_params = None
        self.sym_scenario_params = None

    def build(self, name: str, problem_params: Variables, scenario_params: Variables, output):
        if type(output) == list: # if output is a vector
            output_new = casadi.SX.sym(name, len(output), 1)
            for i, output_i in enumerate(output):
                output_new[i] = output_i
            output = output_new

        function = casadi.Function(name, [problem_params.variables_flat(), scenario_params.variables_flat()], [output])

        zero_input_opt_params = np.zeros([problem_params.n_vars])
        zero_input_scenario = np.zeros([scenario_params.n_vars])

        function(zero_input_opt_params, zero_input_scenario) #Check if function is well defined based on the scenario parameters
        self.name = name
        self.symbolic_output = output
        self.sym_problem_params = problem_params.variables_flat()
        self.sym_scenario_params = scenario_params.variables_flat()
        self.function = function

    def call(self, prob_params=None, scenario_params=None):
        if prob_params is None:
            pp = self.sym_problem_params
        elif type(prob_params) == Variables:
            pp = prob_params.variables_flat()
        else:
            pp = prob_params

        if scenario_params is None:
            sp = self.sym_scenario_params
        elif type(scenario_params) == Variables:
            sp = scenario_params.variables_flat()
        else:
            sp = scenario_params
        return self.function(pp, sp)

    def rebuild(self, opt_params: Variables, scenario_params: Variables):
        """Rebuild the function after opt_params or scenario params in the ocp have chenged."""
        function = casadi.Function(self.name, [opt_params.variables_flat(), scenario_params.variables_flat()], [self.symbolic_output])

        zero_input_opt_params = np.zeros([opt_params.n_vars])
        zero_input_scenario = np.zeros([scenario_params.n_vars])

        function(zero_input_opt_params, zero_input_scenario) #Check if function is well defined based on the scenario parameters
        self.function = function
