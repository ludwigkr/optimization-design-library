import unittest
import sys
sys.path.append("../pybind11_builder/")
sys.path.append("../ipopt_builder/")
sys.path.append("./test_problems")

import hs074_with_params
import build_ipopt
import build_pybind11_module

class TestBuildPyBind11Module(unittest.TestCase):
    def setUp(self):
        pass

    def test_hs074_with_params(self):
        op = hs074_with_params.hs074_problem()
        op = hs074_with_params.add_hs074_build_functions(op)
        ipopt_builder = build_ipopt.IpoptBuilder()
        ipopt_builder.build(op, "hs074_with_params_ipopt")
        build_pybind11_module.export(op, "hs074_with_params_ipopt")
        build_pybind11_module.cmake_insert(op)
        self.assertTrue(True)


if __name__ == "__main__":
    unittest.main()
