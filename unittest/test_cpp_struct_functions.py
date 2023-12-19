
#!/usr/bin/env python3

import sys
sys.path.append("..")
sys.path.append("../helpers")

import casadi
import unittesthelper
import variables
import cpp_struct_functions

import optimizationproblem

class TestCppStructDefintion(unittesthelper.ParserTestCase):
    def setUp(self):
        X = casadi.SX.sym("X")
        self.var = variables.Variables()
        self.var.register("X", X)

        self.op = optimizationproblem.OptimizationProblem()
        self.op.optvars.register("X", X)

    def test_compare_cpp_struct(self):
        result = cpp_struct_functions.compare_cpp_sruct("foo", self.var)

        reference = self.load_reference()
        self.save_reference(result)
        if reference:
            self.assertTrue(result == reference)

    def test_cpp_struct_osstream(self):
        result = cpp_struct_functions.cpp_struct_osstream("foo", self.var)

        reference = self.load_reference()
        self.save_reference(result)
        if reference:
            self.assertTrue(result == reference)

    def test_assign_vector_values_to_struct_entries(self):
        result = cpp_struct_functions.assign_vector_values_to_struct_entries("x", "foo", self.var)

        reference = self.load_reference()
        self.save_reference(result)
        if reference:
            self.assertTrue(result == reference)
