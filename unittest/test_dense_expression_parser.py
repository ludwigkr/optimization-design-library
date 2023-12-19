
import sys
sys.path.append("..")
sys.path.append("../helpers")

import casadi
import unittesthelper
import variables
from parser_common import indent_lines
import dense_expression_parser

import optimizationproblem

class TestDenseExpressionParser(unittesthelper.ParserTestCase):
    def setUp(self):
        self.X = casadi.SX.sym("X", 2, 2)
        self.X[0,0] = 0
        self.X[1,0] = self.X[1,0]**2
        self.X[0,1] = 0

    def test_parse_dense_casadi_expression(self):
        result = dense_expression_parser.parse_dense_casadi_expression("X", self.X)

        reference = self.load_reference()
        self.save_reference(result)
        if reference:
            self.assertTrue(result == reference)

    def test_parse_dense_casadi_expression_one_dimensional(self):
        result = dense_expression_parser.parse_dense_casadi_expression("X", self.X, one_dimensional=True)

        reference = self.load_reference()
        self.save_reference(result)
        if reference:
            self.assertTrue(result == reference)

    def test_parse_empty_list(self):
        result = dense_expression_parser.parse_dense_casadi_expression('X', [])

        reference = self.load_reference()
        self.save_reference(result)
        if reference:
            self.assertTrue(result == reference)



if __name__ == "__main__":
    import unittest
    unittest.main()
