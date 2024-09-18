#!/usr/bin/env python3
import os
import unittest
import casadi
import math
import numpy as np
import test_problems.hs074 as hs074
import test_problems.hs074_with_params as hs074_with_params
import test_problems.nlopt_example as nlopt_example

import sys
sys.path.append("..")
sys.path.append("../helpers")
sys.path.append("../nlopt_builder")
import unittesthelper
import build_nlopt

class TestNloptBuilderCore(unittesthelper.ParserTestCase):
    def setUp(self) -> None:
        self.builder = build_nlopt.NloptBuilder()
        return super().setUp()

    def test_build_xopt_result(self):
        ocp = build_nlopt.OptimizationProblem()
        ocp.optvars.register('number_a')
        ocp.optvars.register('vector_b', 5)
        ocp.optvars.register('matrix_C', [3, 2])

        result = self.builder.build_xopt_result(ocp)

        reference = self.load_reference()
        self.save_reference(result)
        if reference:
            self.assertTrue(result == reference)

    def test_build_nlopt_constraints(self):
        ocp = build_nlopt.OptimizationProblem()
        x = ocp.optvars.register('optvector', 3)

        constr1 = x[0] * x[1]
        ocp.constraints.register('constr1', constr1)

        constr2 = x[1] * x[1]
        ocp.constraints.register('constr1', constr2)

        constr3 = x[2] * x[1]
        ocp.constraints.register('constr1', constr3)

        xinit = ocp.scenario_parameters.register("xinit", 1)

        lbg = casadi.SX.sym("lbg", ocp.constraints.n_constraints)
        lbg[0] = 0
        lbg[1] = math.inf
        lbg[2] = xinit
        ocp.register_lower_inequality_constraint_limits_function(lbg)

        ubg = casadi.SX.sym("lbg", ocp.constraints.n_constraints)
        ubg[0] = 0
        ubg[1] = -math.inf
        ubg[2] = xinit
        ocp.register_upper_inequality_constraint_limits_function(ubg)

        lbx = casadi.SX.sym("lbx", ocp.optvars.n_vars)
        lbx[0] = -math.inf
        lbx[1] = 0
        lbx[2] = xinit
        ocp.register_lower_box_limits_function(lbx)

        ubx = casadi.SX.sym("ubx", ocp.optvars.n_vars)
        ubx[0] = math.inf
        ubx[1] = 0
        ubx[2] = xinit
        ocp.register_upper_box_limits_function(ubx)

        initguess = casadi.SX.sym('x_guess', ocp.optvars.n_vars)
        initguess[:] = 0
        ocp.register_initial_guess_function(initguess)

        result = self.builder.build_nlopt_constraints(ocp)
        result = str(result)

        reference = self.load_reference()
        self.save_reference(result)
        if reference:
            self.assertTrue(result == reference)


class TestNloptExample(unittesthelper.ParserTestCase):
    def setUp(self) -> None:
        self.builder = build_nlopt.NloptBuilder()
        return super().setUp()

    def test_nlopt_example(self):
        ocp = nlopt_example.nlopt_example_problem()
        ocp = nlopt_example.add_nlopt_example_build_functions(ocp)
        self.builder.build(ocp, "./nlopt_example")
        pipe = os.popen("cd nlopt_example && mkdir -p build && cd build && cmake .. && make -j4 && ./test_nlopt-template")
        result = pipe.read()
        pipe.close()
        last_line = result.replace("\n\n", "\n").split("\n")[-2]
        result = last_line.split(' ')[0]
        self.assertTrue(result == "OK")

class TestHS074(unittesthelper.ParserTestCase):
    def setUp(self) -> None:
        self.builder = build_nlopt.NloptBuilder()
        return super().setUp()

    def test_hs074(self):
        ocp = hs074.hs074_problem()
        ocp = hs074.add_hs074_build_functions(ocp)

        with self.subTest("build"):
            self.builder.build(ocp, "./hs074_nlopt")
            pipe = os.popen("cd hs074_nlopt && mkdir -p build && cd build && cmake .. && make -j4 && ./test_hs074-nlopt")
            result = pipe.read()
            pipe.close()
            last_line = result.replace("\n\n", "\n").split("\n")[-2]
            result = last_line.split(' ')[0]
            self.assertTrue(result == "OK")


if __name__ == "__main__":
    unittest.main()
