
import sys
sys.path.append("..")
sys.path.append("../helpers")

import casadi
import unittesthelper
import optimizationproblem
import sparse_expression_parser

class TestSparseExpressionParser(unittesthelper.ParserTestCase):
    def setUp(self):
        self.op = optimizationproblem.OptimizationProblem() #
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
        self.op.objective = X[0,0]**2 + X[1,0]**2
        self.op.constraints.register("c1", X[0,0] * X[1,0])
        self.op.constraints.register("c2", X[0,0] + X[1,0])
        self.op.build_lagrangian()

        self.E = casadi.SX.sym("E", 2, 2)
        self.E[0,0] = 0
        self.E[1,0] = 1
        self.E[0,1] = 2
        self.E[1,1] = 3

        self.X = casadi.SX.sym("X", 2, 2)
        self.X[0,0] = 0
        self.X[1,0] = self.X[1,0]**2
        self.X[0,1] = 0

    def test_parse_sparse_casadi_expression(self):
        result_index, result_value = sparse_expression_parser.parse_sparse_casadi_expression("foo", self.op.lagrangian_hessian)
        result = result_index + result_value

        reference = self.load_reference()
        self.save_reference(result)
        if reference:
            self.assertTrue(result == reference)

    def test_parse_sparse_casadi_expression_E(self):
        result_index, result_value = sparse_expression_parser.parse_sparse_casadi_expression("E", self.E)
        result = result_index + result_value

        reference = self.load_reference()
        self.save_reference(result)
        if reference:
            self.assertTrue(result == reference)

    def test_parse_sparse_casadi_expression_lower_triangular_shape(self):
        result_index, result_value = sparse_expression_parser.parse_sparse_casadi_expression("foo", self.op.lagrangian_hessian, has_lower_triangular_shape=True)
        result = result_index + result_value

        reference = self.load_reference()
        self.save_reference(result)
        if reference:
            self.assertTrue(result == reference)


if __name__ == "__main__":
    import unittest
    unittest.main()
