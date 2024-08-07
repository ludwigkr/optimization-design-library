#!/usr/bin/env python

import sys
import unittest
import casadi
import numpy as np

sys.path.append('../')
sys.path.append('../min_nlp')
sys.path.append('../min_nlp_with_params')
from optimizationproblem import OptimizationProblem

from variables import Variables
from function import Function
from constraints import Constraints
from quadratic_optimizer_elements import QuadraticOptimizerElements

class TestFunctions(unittest.TestCase):

    def setUp(self):
        self.ocp = OptimizationProblem()
        self.X = self.ocp.optvars.register("X", [2,1])
        self.ocp.scenario_parameters.register("scenario1")

    def test_function(self):
        fn = Function()

        # Undefined function
        param1 = self.ocp.problem_parameters.register('param1')
        x = self.ocp.optvars.variables_by_names('X')
        output = param1 * x
        try:
            fn.build('fn', self.ocp.problem_parameters, self.ocp.scenario_parameters, output)
            self.assertFalse(True)
        except RuntimeError:
            self.assertFalse(False)

       # Proper function
        scenario1 = self.ocp.scenario_parameters.variables_by_names('scenario1')
        output = param1 * scenario1
        try:
            fn.build('fn', self.ocp.problem_parameters, self.ocp.scenario_parameters, output)
            self.assertTrue(True)
        except RuntimeError:
            self.assertTrue(False)

        # Function call
        pv = 1
        s = 2
        res = fn.call(pv, s)
        self.assertTrue(type(res) == casadi.DM)
        self.assertTrue(res == 2)

        # Overwrite function
        output = [scenario1+param1, scenario1*param1]
        try:
            fn.build('fn', self.ocp.problem_parameters, self.ocp.scenario_parameters, output)
            self.assertTrue(True)
        except RuntimeError:
            self.assertTrue(False)

        res = fn.call(pv, s)
        self.assertTrue(np.linalg.norm(np.array(res) - np.array([[3], [2]])) < 1e-3)

        # Rebuild function (when problem parameter or scenario parameter have changed)
        scenario_extended = self.ocp.scenario_parameters.register('scenario_extended')
        scenario_extended = self.ocp.problem_parameters.register('problem_extended')

        fn.rebuild(self.ocp.problem_parameters, self.ocp.scenario_parameters)

        pv = [1, 2]
        s = [2, 100]

        res = fn.call(pv, s)
        self.assertTrue(np.linalg.norm(np.array(res) - np.array([[3], [2]])) < 1e-3)

        # Function call symbolic:
        res = fn.call()

        self.assertTrue(res[0] == output[0])
        self.assertTrue(res[1] == output[1])

        fn = Function()
        fn.build('fn', self.ocp.problem_parameters, self.ocp.scenario_parameters, np.array([[1], [2]]))
        # res = fn()
        # print(res)

if __name__ == '__main__':
    unittest.main()
