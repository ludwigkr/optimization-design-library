#!/usr/bin/env python3
import sys
sys.path.append("..")
sys.path.append("../helpers")

import casadi
import unittesthelper
import unittest
from variables import Variables
from optimizationproblem import OptimizationProblem
import cpp_optimizer_helper

class TestCppOptimizerHelper(unittesthelper.ParserTestCase):
    def setUp(self):
        self.op = OptimizationProblem() #
        self.op.optvars.register("X", [2,1])
        self.op.optvars.register("Y")

        self.op.problem_parameters.register("A", [2,1])
        self.op.problem_parameters.register("B")
        self.op.scenario_parameters.register("C", [2,1])
        self.op.scenario_parameters.register("D")

        self.exp1 = \
"""X[0,0] = C_0+X_0*X_1;
X[0,1] = A_0*X_1;
X[1,0] = sq(X_1);
X[1,1] = X_0;
"""

    def test_build_mappers(self):
        result = cpp_optimizer_helper.build_mappers(self.op)

        reference = self.load_reference()
        self.save_reference(result)
        if reference:
            self.assertTrue(result == reference)

    def test_substitude_optimization_variables_pparam_as_struct(self):
        result = cpp_optimizer_helper.substitude_optimization_variables(self.exp1, self.op, True)

        reference = self.load_reference()
        self.save_reference(result)
        if reference:
            self.assertTrue(result == reference)

    def test_substitude_optimization_variables(self):
        result = cpp_optimizer_helper.substitude_optimization_variables(self.exp1, self.op, False)

        reference = self.load_reference()
        self.save_reference(result)
        if reference:
            self.assertTrue(result == reference)

    def test_build_osstreams(self):
        result = cpp_optimizer_helper.build_osstreams(self.op)

        reference = self.load_reference()
        self.save_reference(result)
        if reference:
            self.assertTrue(result == reference)

    def test_build_operators(self):
        result = cpp_optimizer_helper.build_operators(self.op)

        reference = self.load_reference()
        self.save_reference(result)
        if reference:
            self.assertTrue(result == reference)

if __name__ == "__main__":
    unittest.main()
