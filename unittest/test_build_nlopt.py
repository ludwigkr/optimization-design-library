#!/usr/bin/env python3
import os
import unittest
import numpy as np
import test_problems.hs074 as hs074
import test_problems.hs074_with_params as hs074_with_params

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
