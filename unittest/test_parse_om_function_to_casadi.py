#!/usr/bin/env python3
import unittest
import sys
import casadi
import numpy as np

sys.path.append("..")
sys.path.append("../openmodelica_parser")
from variables import Variables
from model_variables import ModelVariables
from parse_om_function_to_casadi import parse_om_function_to_casadi

class TestParseOMFunctionToCasadi(unittest.TestCase):
    def setUp(self):
        self.x = Variables()
        self.x.register('spring2_s_rel')
        self.x.register('spring2_s_rel0')
        self.u = Variables()
        self.params = Variables()
        self.params.register('spring2_c')
        self.model_vars = ModelVariables(self.x, self.u, self.params)

    def test_parse_om_function_to_casadi(self):
        func = parse_om_function_to_casadi(self.model_vars, "spring2_c * (spring2_s_rel - spring2_s_rel0);")
        self.assertTrue(type(func) == casadi.Function)
        func = parse_om_function_to_casadi(self.model_vars, "spring2_c * (spring2_s_rel - spring2_s_rel0)")
        self.assertTrue(type(func) == casadi.Function)

    def test_om_function_features(self):
        func = parse_om_function_to_casadi(self.model_vars, "spring2_c * (spring2_s_rel - spring2_s_rel0)")

        with self.subTest("Vector handling"):
            # Each new state gets it's own row
            X = np.array([[3,2], [1,1]])
            U = []
            Params = np.array([.5])
            result = func(X, U, Params)
            result = np.array(result)
            error = np.linalg.norm(np.array([1., 0.5]) - result)
            self.assertTrue( error < 1e-3)

if __name__ == "__main__":
    unittest.main()
