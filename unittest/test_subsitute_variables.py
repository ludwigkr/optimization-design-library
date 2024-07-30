#!/usr/bin/env python3
import sys
sys.path.append("..")
sys.path.append("../helpers")

import unittest
import unittesthelper
import substitute_variables
from variables import Variables

import optimizationproblem

class TestCppStructDefintion(unittesthelper.ParserTestCase):
    def setUp(self):
        pass

    def test_substitute_variable_with_exp1(self):
        exp1 = \
"""float X_temporary1 = 0;
X[0,0] = X_temporary1;
X[0,1] = X_temporary1;
X[1,0] = sq(X_1);
X[1,1] = X_0;
"""
        result = substitute_variables.substitute_variable(exp1, "X", "xopt", 2)

        reference = self.load_reference()
        self.save_reference(result)
        if reference:
            self.assertTrue(result == reference)


    def test_subsitute_variables(self):
        vars = Variables()
        A = vars.register('A', [2, 2])
        B = vars.register('B', [2, 2])
        exp = \
"""
A_3 + B_3
"""
        struct_name = 'res'
        link_symbol = '.'

        result = substitute_variables.substitute_variable_in_struct(exp, struct_name, link_symbol, vars)

        reference = self.load_reference()
        self.save_reference(result)
        if reference:
            self.assertTrue(result == reference)


if __name__ == "__main__":
    unittest.main()
