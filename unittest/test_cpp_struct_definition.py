#!/usr/bin/env python3

import sys
sys.path.append("..")
sys.path.append("../helpers")

import casadi
import unittesthelper
import variables
import cpp_struct_definition


class TestCppStructDefintion(unittesthelper.ParserTestCase):
    def setUp(self):
        X = casadi.SX.sym("X")
        self.var = variables.Variables()
        self.var.register("X", X)

    def test_cpp_struct_definition(self):
        result = cpp_struct_definition.cpp_struct_definition("optimization_variable", self.var)

        reference = self.load_reference()
        self.save_reference(result)
        if reference:
            self.assertTrue(result == reference)

    def test_empty_variables(self):
        result = cpp_struct_definition.cpp_struct_definition("problem_parameter", variables.Variables())
        self.save_reference(result)
