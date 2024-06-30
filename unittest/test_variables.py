#!/usr/bin/env python

import unittest
import casadi
import numpy as np
import sys
sys.path.append("..")
from variables import Variables
from unittesthelper import ParserTestCase

class TestVariables(ParserTestCase):

    def setUp(self):
        self.X = casadi.SX.sym("X", 2, 1)
        self.scenario = casadi.SX.sym("scenario")

        self.var = Variables()
        self.var.register("var1", [2,1])
        self.var.register("var2", [2,1])

    def test_variables(self):
        var = Variables()
        check = var.variables_flat()
        self.assertTrue(isinstance(check, list))

        var.register("X", [2,1])
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

        Y = var.register("Y", [2,1])
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

    def test_unpacked(self):
        v = Variables()
        v.register('a')
        v.register('b', 2)

        res = v.unpacked([1, [1,2]])
        self.assertTrue(True)

    def test_assign_values(self):
        with self.subTest("packed"):
            data = self.var.unpacked([[1,2], [3,4]])
            packed = self.var.packed(data)
            self.assertTrue(packed[0][0] == 1)

    def test_variables_by_names(self):
        with self.subTest("with_string_argument"):
            result = str(self.var.variables_by_names('var2'))

        with self.subTest("with_list_arguments"):
            self.var.register("var3", [2,1])
            result += str(self.var.variables_by_names(['var2', 'var3']))

        with self.subTest("non existing argument"):
            self.assertRaises(AssertionError, self.var.variables_by_names, "var4")

        reference = self.load_reference()
        self.save_reference(result)
        if reference:
            self.assertTrue(result == reference)

    def test_remove(self):
        self.var.register('var3',3)
        self.var.remove('var1')
        self.assertTrue(len(self.var.idxs) == 2)
        self.assertTrue(len(self.var.names) == 2)
        self.assertTrue(len(self.var.variables) == 2)
        self.assertTrue(np.all(self.var.idxs['var2'] == np.array([[0],[1]])))
        self.assertTrue(np.all(self.var.idxs['var3'] == np.array([[2],[3], [4]])))
        self.assertTrue(self.var.n_vars == 5)



if __name__ == '__main__':
    unittest.main()
