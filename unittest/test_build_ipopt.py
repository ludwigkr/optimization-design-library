import os
import unittest
import numpy as np
import test_problems.hs074 as hs074

import sys
sys.path.append("..")
sys.path.append("../helpers")
sys.path.append("../ipopt_builder")
import unittesthelper
import build_ipopt
import quadratic_optimizer_elements
import optimizationconfiguration as optconfig
import optimizationsolver


class TestBuildIpopt(unittesthelper.ParserTestCase):
    def setUp(self) -> None:
        self.builder = build_ipopt.IpoptBuilder()
        return super().setUp()

    def test_hs074(self):
        ocp = hs074.hs074_problem()
        ocp = hs074.add_hs074_build_functions(ocp)
        quadratic_elements = quadratic_optimizer_elements.QuadraticOptimizerElements(ocp)

        with self.subTest("run"):        
            x_ = np.array([1., 5. , 5., 1.], dtype=float)
            scenario = ocp.scenario_parameters.unpacked([x_])

            opts = optconfig.load_optimizer_settings("ipopt")
            solver = optimizationsolver.build_solver(ocp, opts)

            result = optimizationsolver.run(solver, ocp, scenario)

            Xopt = result["x"]
            print("xopt: ", ocp.optvars.packed(Xopt))
            Xreal_opt = np.array([[1.00000000, 4.74299963, 3.82114998, 1.37940829]]).T

            self.assertTrue(np.linalg.norm(np.array(Xopt) - Xreal_opt) < 1e-5)

            case_exporter = optimizationsolver.TestCaseExporter()
            case_exporter.add_case(ocp, scenario, [], result)
            case_exporter.save(self.json_file_path())

        with self.subTest("build"):
            self.builder.build(ocp, quadratic_elements, "./hs074_ipopt")
            pipe = os.popen("cd hs074_ipopt && mkdir -p build && cd build && cmake .. && make -j4 && ./test_hs074")
            result = pipe.read()
            pipe.close()
            last_line = result.replace("\n\n", "\n").split("\n")[-2]
            result = last_line.split(' ')[0]
            self.assertTrue(result == "OK")


if __name__ == "__main__":
    unittest.main()
