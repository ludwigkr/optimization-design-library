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
from ocp_min_nlp_with_params import optimization_problem_min_nlp_with_params
from qpelements import QuadraticOptimizerElements

from problembuildhelper import ProblemBuildHelper

class TestFunctions(unittest.TestCase):

    def setUp(self):
        self.X = casadi.SX.sym("X", 2, 1)
        self.scenario = casadi.SX.sym("scenario")
        self.ocp = OptimizationProblem()
        self.ocp.optvars.register("X", self.X)
        self.ocp.scenario_parameters.register("scenario", self.scenario)

    def test_function(self):
        fn = Function()
        p = casadi.SX.sym('p')

        # Undefined function
        self.ocp.problem_parameters.register('p', p)
        x = self.ocp.optvars.block_by_name('X')
        output = p * x
        try:
            fn.build('fn', self.ocp.problem_parameters, self.ocp.scenario_parameters, output)
            self.assertFalse(True)
        except RuntimeError:
            self.assertFalse(False)

       # Proper function
        scenario = self.ocp.scenario_parameters.block_by_name('scenario')
        output = p * scenario
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
        output = [scenario+p, scenario*p]
        try:
            fn.build('fn', self.ocp.problem_parameters, self.ocp.scenario_parameters, output)
            self.assertTrue(True)
        except RuntimeError:
            self.assertTrue(False)

        res = fn.call(pv, s)
        self.assertTrue(np.linalg.norm(np.array(res) - np.array([[3], [2]])) < 1e-3)

        # Rebuild function (when problem parameter or scenario parameter have changed)
        scenario_extended = casadi.SX.sym('scenario_extended')
        problemp_extended = casadi.SX.sym('problemp_extended')
        self.ocp.scenario_parameters.register('scenario_extended', scenario_extended)
        self.ocp.problem_parameters.register('problemp_extended', problemp_extended)

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
