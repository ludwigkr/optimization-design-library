#!/usr/bin/env python

import unittest
import casadi
import numpy as np
import sys
sys.path.append("..")
from variables import Variables

class TestVariables(unittest.TestCase):

    def setUp(self):
        self.X = casadi.SX.sym("X", 2, 1)
        self.scenario = casadi.SX.sym("scenario")

        self.var = Variables()
        var1 = casadi.SX.sym('var1', 2, 1)
        self.var.register("var1", var1)
        var2 = casadi.SX.sym('var2', 2, 1)
        self.var.register("var2", var2)

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

    def test_assign_values(self):
        with self.subTest("packed"):
            data = self.var.unpacked([[1,2], [3,4]])
            packed = self.var.packed(data)
            self.assertTrue(packed[0][0] == 1)

        with self.subTest("buggy variable decleration"):
            """If variables var1 and var2 are not symbolic, this leads to error.
                   Compare against packed-subtest."""
            var = Variables()
            var1 = casadi.SX(2, 1)
            var.register("var1", var1)
            var2 = casadi.SX(2, 1)
            var.register("var2", var2)
            data = var.unpacked([[1,2], [3,4]])
            packed = var.packed(data)
            self.assertFalse(packed[0][0] == 1)

if __name__ == '__main__':
    unittest.main()
