
import sys
sys.path.append("..")
sys.path.append("../helpers")

import casadi
import unittesthelper
from parser_common import indent_lines
import scalar_expression_parser

class TestScalarExpressionParser(unittesthelper.ParserTestCase):
    def setUp(self):
        X = casadi.SX.sym("X", 2, 1)
        self.exp = X[0,0] + 3.1415*X[1,0]**2 + X[0,0]**0.5

    def test_parse_scalar_casadi_expression(self):
        result = scalar_expression_parser.parse_scalar_casadi_expression("foo", self.exp)

        reference = self.load_reference()
        self.save_reference(result)
        if reference:
            self.assertTrue(result == reference)



if __name__ == "__main__":
    import unittest
    unittest.main()
