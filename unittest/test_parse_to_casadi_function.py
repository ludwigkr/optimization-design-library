#!/usr/bin/env python3
import unittest
import sys
import casadi
import numpy as np

sys.path.append("..")
sys.path.append("../openmodelica_parser")
from variables import Variables
from model_variables import ModelVariables
from parse_to_casadi_function import parse_to_casadi_function

class TestParseToCasadiFunction(unittest.TestCase):
    def setUp(self):
        self.x = Variables()
        self.x.register('value_b')
        self.x.register('value_a')
        self.u = Variables()
        self.params = Variables()
        self.params.register('value_c')
        self.model_vars = ModelVariables()
        self.model_vars.states = self.x
        self.model_vars.inputs = self.u
        self.model_vars.parameters = self.params

    def test_parse_om_function_to_casadi(self):
        func = parse_to_casadi_function(self.model_vars, "value_c * (value_b - value_a);")
        self.assertTrue(type(func) == casadi.Function)
        func = parse_to_casadi_function(self.model_vars, "value_c * (value_b - value_a)")
        self.assertTrue(type(func) == casadi.Function)

    def test_parse_function_with_numbers_to_casadi(self):
        func = parse_to_casadi_function(self.model_vars, "value_c * (2./value_b - value_a);")
        x = self.x.unpacked([1,0.3])
        u = []
        p = self.params.unpacked([0.4])
        ret = func(x,u,p)
        self.assertTrue(ret == 0.68)
        self.assertTrue(type(func) == casadi.Function)

    def test_om_function_features(self):
        func = parse_to_casadi_function(self.model_vars, "value_c * (value_b - value_a)")

        with self.subTest("Vector handling"):
            # Each new state gets it's own row
            X = np.array([[3,2], [1,1]])
            U = []
            Params = np.array([.5])
            result = func(X, U, Params)
            result = np.array(result)
            error = np.linalg.norm(np.array([1., 0.5]) - result)
            self.assertTrue( error < 1e-3)

    def test_dynamic_of_PT1v2(self):
        model_vars = ModelVariables()
        model_vars.parameters = ['T11', 'K11', 'u0_11']
        model_vars.inputs = ['u1']
        model_vars.states = ['x11']
        model_vars.convert_variables_to_symbolics()
        func = parse_to_casadi_function(model_vars, "-1.0 / T11 * x11 + K11 / T11 * (u1 + u0_11);")
        ret = func(1, 2, np.array([3,4,5]))
        self.assertTrue(ret is not np.nan)
        pass


if __name__ == "__main__":
    unittest.main()
