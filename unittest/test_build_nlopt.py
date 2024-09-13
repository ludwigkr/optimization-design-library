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
import optimizationconfiguration as optconfig
import optimizationsolver
from quadratic_optimizer_elements import QuadraticOptimizerElements
import testcase_exporter

class TestNloptBuilderCore(unittesthelper.ParserTestCase):
    def setUp(self) -> None:
        self.builder = build_nlopt.NloptBuilder()
        return super().setUp()

    @unittest.skip("not ready yet")
    def test_build_xopt_struct(self):
        ocp = build_nlopt.OptimizationProblem()
        ocp.optvars.register('number_a')
        ocp.optvars.register('vector_b', 5)
        ocp.optvars.register('matrix_C', [2, 2])

        result = self.builder.build_xopt_struct(ocp)
        
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


class TestHS074(unittesthelper.ParserTestCase):
    def setUp(self) -> None:
        self.builder = build_nlopt.NloptBuilder()
        return super().setUp()

    def test_hs074(self):
        ocp = hs074.hs074_problem()
        ocp = hs074.add_hs074_build_functions(ocp)

        # with self.subTest("run"):
        #     x_ = np.array([1., 5. , 5., 1.], dtype=float)
        #     scenario = ocp.scenario_parameters.unpacked([x_])

        #     opts = optconfig.load_optimizer_settings("ipopt")
        #     solver = optimizationsolver.build_solver(ocp, opts)

        #     result = optimizationsolver.run(solver, ocp, scenario)

        #     Xopt = result["x"]
        #     print("xopt: ", ocp.optvars.packed(Xopt))
        #     Xreal_opt = np.array([[1.00000000, 4.74299963, 3.82114998, 1.37940829]]).T

        #     self.assertTrue(np.linalg.norm(np.array(Xopt) - Xreal_opt) < 1e-5)

        #     case_exporter = testcase_exporter.TestCaseExporter()
        #     case_exporter.add_case(ocp, scenario, [], result)
        #     case_exporter.save(self.json_file_path())


        with self.subTest("build"):
            self.builder.build(ocp, "./hs074_nlopt")
            # pipe = os.popen("cd hs074_ipopt && mkdir -p build && cd build && cmake .. && make -j4 && ./test_hs074")
            # result = pipe.read()
            # pipe.close()
            # last_line = result.replace("\n\n", "\n").split("\n")[-2]
            # result = last_line.split(' ')[0]
            # self.assertTrue(result == "OK")
            pass

class TestHS074withParams(unittesthelper.ParserTestCase):
    def setUp(self) -> None:
        self.builder = build_nlopt.NloptBuilder()
        self.ocp = hs074_with_params.hs074_problem()
        self.ocp = hs074_with_params.add_hs074_build_functions(self.ocp)
        self.ocp.build_lagrangian()
        self.qoe = QuadraticOptimizerElements(self.ocp)
        return super().setUp()

    # def test_build_objective(self):
    #     objective = self.builder.build_objective(self.ocp)
    #     print(objective)
    #     pass



    # def test_hs074_with_params(self):

    #     with self.subTest("run"):
    #         x_ = np.array([1., 5. , 5., 1.], dtype=float)
    #         scenario = self.ocp.scenario_parameters.unpacked([x_])
    #         params = self.ocp.problem_parameters.unpacked([0])

    #         opts = optconfig.load_optimizer_settings("ipopt")
    #         solver = optimizationsolver.build_solver(self.ocp, opts)

    #         result = optimizationsolver.run(solver, self.ocp, scenario, params)

    #         Xopt = result["x"]
    #         print("xopt: ", self.ocp.optvars.packed(Xopt))
    #         Xreal_opt = np.array([[1.00000000, 4.74299963, 3.82114998, 1.37940829]]).T

    #         self.assertTrue(np.linalg.norm(np.array(Xopt) - Xreal_opt) < 1e-5)

    #         case_exporter = testcase_exporter.TestCaseExporter()
    #         case_exporter.add_case(self.ocp, scenario, params, result)
    #         case_exporter.save(self.json_file_path())

        with self.subTest("build"):
            self.builder.build(self.ocp, "./hs074_with_params_nlopt")
            # pipe = os.popen("cd hs074_with_params_ipopt && mkdir -p build && cd build && cmake .. && make -j4 && ./test_hs074")
            # result = pipe.read()
            # pipe.close()
            # last_line = result.replace("\n\n", "\n").split("\n")[-2]
            # result = last_line.split(' ')[0]
            # self.assertTrue(result == "OK")


if __name__ == "__main__":
    unittest.main()
