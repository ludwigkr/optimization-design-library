#!/usr/bin/env python
import unittest
import casadi
import numpy as np
import sys
sys.path.append("..")
from math_helper import symetric_based_on_numeric


class TestCasadi(unittest.TestCase):

    def setUp(self):
        self.X = casadi.SX.sym("X", 2, 1)
        self.scenario = casadi.SX.sym("scenario")

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

    @unittest.skip("Not working")
    def test_symetric_check_on_expression(self):
        X = casadi.SX.sym("X", 2, 1)
        mat = casadi.SX.sym("mat", 2, 2)

        with self.subTest("symetric"):
            mat[0, 0] = X[0]
            mat[1, 0] = X[0]*X[1]
            mat[0, 1] = X[1]*X[0]
            mat[1, 1] = X[1]
            self.assertTrue(str(mat[1, 0]) == str(mat[0, 1]))
            self.assertTrue(str(mat) == str(mat.T))

    def test_symetric_check_on_numeric(self):
        X = casadi.SX.sym("X", 2, 1)
        mat = casadi.SX.sym("mat", 2, 2)

        with self.subTest("symetric"):
            mat[0, 0] = X[0]
            mat[1, 0] = X[0]*X[1]
            mat[0, 1] = X[1]*X[0]
            mat[1, 1] = X[1]
            self.assertTrue(symetric_based_on_numeric(mat, [X, [], []]))

        with self.subTest("non-symetric"):
            mat[0, 0] = X[0]
            mat[1, 0] = X[0]*2
            mat[0, 1] = X[1]*X[0]
            mat[1, 1] = X[1]
            self.assertFalse(symetric_based_on_numeric(mat, [X, [], []]))

if __name__ == '__main__':
    unittest.main()
