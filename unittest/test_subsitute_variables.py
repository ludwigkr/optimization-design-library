#!/usr/bin/env python3
import sys
sys.path.append("..")
sys.path.append("../helpers")

import unittest
import unittesthelper
import substitute_variables

import optimizationproblem

class TestCppStructDefintion(unittesthelper.ParserTestCase):
    def setUp(self):
        self.exp1 = \
"""float X_temporary1 = 0;
X[0,0] = X_temporary1;
X[0,1] = X_temporary1;
X[1,0] = sq(X_1);
X[1,1] = X_0;
"""

    def test_substitute_variable_with_exp1(self):
        result = substitute_variables.substitute_variable(self.exp1, "X", "xopt", 2)

        reference = self.load_reference()
        self.save_reference(result)
        if reference:
            self.assertTrue(result == reference)


if __name__ == "__main__":
    unittest.main()
