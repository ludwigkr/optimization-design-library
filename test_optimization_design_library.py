#!/usr/bin/env python

import sys
import unittest
import casadi
import numpy as np

sys.path.append('./min_nlp')
sys.path.append('./min_nlp_with_params')
from optimizationproblem import OptimizationProblem

from variables import Variables
from function import Function
from constraints import Constraints
from ocp_min_nlp_with_params import optimization_problem_min_nlp_with_params
from qpelements import QuadraticOptimizerElements

from problembuildhelper import ProblemBuildHelper

class TestOptimizationProblem(unittest.TestCase):

    def setUp(self):
        self.X = casadi.SX.sym("X", 2, 1)
        self.scenario = casadi.SX.sym("scenario")
        self.ocp = OptimizationProblem()
        self.ocp.optvars.register("X", self.X)
        self.ocp.scenario_parameter.register("scenario", self.scenario)

    def test_variables(self):
        var = Variables()
        check = var.variables_flat()
        self.assertTrue(isinstance(check, list))

        var.register("X", self.X)
        check = var.variables_flat()
        self.assertTrue(isinstance(check, casadi.SX))

        x0 = np.array([2, 1])
        check = var.unpacked(x0)
        self.assertTrue(isinstance(check, np.ndarray))
        self.assertTrue(check[0] == 2)
        self.assertTrue(check[1] == 1)

        x0 = np.array([[2], [1]])
        check = var.packed(x0)
        self.assertTrue(isinstance(check, casadi.DM))

        check = var.unpacked()
        self.assertTrue(isinstance(check, casadi.SX))

        Y = casadi.SX.sym("Y", 2, 1)
        var.register("Y", Y)
        data0 = [[2., 1], [0., 3]]
        check = var.unpacked(data0)
        self.assertTrue(isinstance(check, np.ndarray))
        self.assertTrue(check.size == 4)
        self.assertTrue(check[0] == 2)
        self.assertTrue(check[1] == 1)

        check = var.unpacked()
        self.assertTrue(isinstance(check, casadi.SX))
        self.assertTrue(check.size() == (4, 1))

        data0 = np.array([2., 1, 0, 4])
        check = var.packed(data0)

    def test_casadi_functions(self):
        """
        Testing casadi function functionality.

        Testing properties of casadi this project work with.
        """
        # Well defined function
        # - output vector is of type casadi.DM
        x = casadi.SX.sym('x', 2)
        y = casadi.SX.sym('y')
        f = casadi.Function('f', [x, y], [casadi.sin(y)*x])
        self.assertTrue(f.n_in() == 2)
        self.assertTrue(f.nnz_in() == 3)
        self.assertTrue(f.n_out() == 1)

        x0 = np.array([1, 0])
        y0 = 2
        res = f(x0, y0)
        self.assertTrue(type(res) == casadi.DM)
        self.assertTrue(np.linalg.norm(np.array(res) - np.array([[0.909297], [0]])) < 1e-3)

        # Special case: No input vector
        # - output vector is a dict
        output = np.array([[2], [1]])
        output = casadi.DM(output)
        f = casadi.Function('f', [], [output])
        self.assertTrue(f.n_in() == 0)
        self.assertTrue(f.n_out() == 1)

        res = f()
        self.assertTrue(type(res) == dict)
        res = res['o0']
        self.assertTrue(np.linalg.norm(np.array(res) - np.array([[2], [1]])) < 1e-3)

        # Special case: No input vector
        # if input variables are not given, casadi sets them to 0
        f = casadi.Function('f', [[], x], [2*x])
        self.assertTrue(f.n_in() == 2)
        self.assertTrue(f.nnz_in() == 2)
        self.assertTrue(f.n_out() == 1)
        res = f()

    def test_function(self):
        fn = Function()
        p = casadi.SX.sym('p')

        # Undefined function
        self.ocp.problem_parameter.register('p', p)
        x = self.ocp.optvars.block_by_name('X')
        output = p * x
        try:
            fn.build('fn', self.ocp.problem_parameter, self.ocp.scenario_parameter, output)
            self.assertFalse(True)
        except RuntimeError:
            self.assertFalse(False)

       # Proper function
        scenario = self.ocp.scenario_parameter.block_by_name('scenario')
        output = p * scenario
        try:
            fn.build('fn', self.ocp.problem_parameter, self.ocp.scenario_parameter, output)
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
            fn.build('fn', self.ocp.problem_parameter, self.ocp.scenario_parameter, output)
            self.assertTrue(True)
        except RuntimeError:
            self.assertTrue(False)

        res = fn.call(pv, s)
        self.assertTrue(np.linalg.norm(np.array(res) - np.array([[3], [2]])) < 1e-3)

        # Rebuild function (when problem parameter or scenario parameter have changed)
        scenario_extended = casadi.SX.sym('scenario_extended')
        problemp_extended = casadi.SX.sym('problemp_extended')
        self.ocp.scenario_parameter.register('scenario_extended', scenario_extended)
        self.ocp.problem_parameter.register('problemp_extended', problemp_extended)

        fn.rebuild(self.ocp.problem_parameter, self.ocp.scenario_parameter)

        pv = [1, 2]
        s = [2, 100]

        res = fn.call(pv, s)
        self.assertTrue(np.linalg.norm(np.array(res) - np.array([[3], [2]])) < 1e-3)

        # Function call symbolic:
        res = fn.call()

        self.assertTrue(res[0] == output[0])
        self.assertTrue(res[1] == output[1])

        fn = Function()
        fn.build('fn', self.ocp.problem_parameter, self.ocp.scenario_parameter, np.array([[1], [2]]))
        # res = fn()
        # print(res)


class TestProblemBuildHelper(unittest.TestCase):
    def setUp(self):
        self.var = Variables()
        X = casadi.SX.sym("X", 2, 1)
        Y = casadi.SX.sym("Y", 2, 1)
        self.var.register("X", X)
        self.var.register("Y", Y)
        self.problem_build_helper = ProblemBuildHelper()
        self.op = optimization_problem_min_nlp_with_params()
        self.test_op = OptimizationProblem()
        self.test_op.optvars.register("X", X)
        self.test_op.optvars.register("Y", Y)
        self.test_op.objective = X**2 + Y**2
        self.quadratic_elements = QuadraticOptimizerElements(self.test_op)


    def test_variable_structure(self):
        output = self.problem_build_helper.variable_structure_definition("problem_parameter", self.var)
        target_output = \
"""struct problem_parameter{
    Eigen::VectorXd X;
    Eigen::VectorXd Y;

    problem_parameter(Eigen::VectorXd _X, Eigen::VectorXd _Y):
        X(_X),
        Y(_Y){}

};"""
        self.assertTrue(target_output == output)

    def test_substitude_variable(self):
        ret = self.problem_build_helper.build_dense_matrix('H', self.quadratic_elements.objective_jacobian)
        ret = self.problem_build_helper.substitude_variable(ret, 'X', 'xopt', self.op.optvars.n_vars)
        ret = self.problem_build_helper.substitude_variable(ret, 'Y', 'xopt', self.op.optvars.n_vars, self.test_op.optvars.idxs['Y'][0,0])
        target_output = \
"""    H[0] = (xopt[0]+xopt[0]);
    H[5] = (xopt[1]+xopt[1]);
    H[8] = (xopt[2]+xopt[2]);
    H[13] = (xopt[3]+xopt[3]);"""
        self.assertTrue(ret == target_output)



if __name__ == '__main__':
    unittest.main()
