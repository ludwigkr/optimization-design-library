#!/usr/bin/env python3
import sys
sys.path.append("..")
sys.path.append("../helpers")

import casadi
import unittesthelper
import variables
import problembuildhelper
from variables import Variables
from optimizationproblem import OptimizationProblem
import cpp_optimizer_helper

class TestCppOptimizerHelper(unittesthelper.ParserTestCase):
    def setUp(self):
        self.op = OptimizationProblem() #
        X = casadi.SX.sym("X", 2, 1)
        self.op.optvars.register("X", X)
        Y = casadi.SX.sym("Y")
        self.op.optvars.register("Y", Y)
        A = casadi.SX.sym("A", 2, 1)
        self.op.problem_parameters.register("A", A)
        B = casadi.SX.sym("B")
        self.op.problem_parameters.register("B", B)
        C = casadi.SX.sym("C", 2, 1)
        self.op.scenario_parameters.register("C", C)
        D = casadi.SX.sym("D")
        self.op.scenario_parameters.register("D", D)


    def test_streamline_identical(self):
        helper = problembuildhelper.ProblemBuildHelper()
        old = helper.build_mappers(self.op)
        new = cpp_optimizer_helper.build_mappers(self.op)
        self.save_result(old, new)
        self.assertTrue(old == new)

    def test_build_mappers(self):
        result = cpp_optimizer_helper.build_mappers(self.op)

        reference = self.load_reference()
        self.save_reference(result)
        if reference:
            self.assertTrue(result == reference)
