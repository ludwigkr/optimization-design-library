#!/usr/bin/env python

import sys
sys.path.append("..")
sys.path.append("../min_nlp_with_params")
import unittest
import casadi
import numpy as np

sys.path.append('./min_nlp')
sys.path.append('./min_nlp_with_params')
from optimizationproblem import OptimizationProblem

from variables import Variables
from ocp_min_nlp_with_params import optimization_problem_min_nlp_with_params
from qpelements import QuadraticOptimizerElements

from problembuildhelper import ProblemBuildHelper


class TestProblemBuildHelper(unittest.TestCase):
    def setUp(self):
        self.var = Variables()
        X = casadi.SX.sym("X", 2, 1)
        Y = casadi.SX.sym("Y", 2, 1)
        self.var.register("X", X)
        self.var.register("Y", Y)
        self.problem_build_helper = ProblemBuildHelper()
        self.op = optimization_problem_min_nlp_with_params()
        self.test_op = OptimizationProblem()
        self.test_op.optvars.register("X", X)
        self.test_op.optvars.register("Y", Y)
        self.test_op.objective = X**2 + Y**2
        self.quadratic_elements = QuadraticOptimizerElements(self.test_op)


    def test_variable_structure(self):
        output = self.problem_build_helper.variable_structure_definition("problem_parameter", self.var)
        target_output = \
"""struct problem_parameter{
    Eigen::VectorXd X;
    Eigen::VectorXd Y;

    problem_parameter(Eigen::VectorXd _X, Eigen::VectorXd _Y):
        X(_X),
        Y(_Y){}

};"""
        self.assertTrue(target_output == output)

    def test_substitude_variable(self):
        ret = self.problem_build_helper.build_matrix('H', self.quadratic_elements.objective_jacobian)
        ret = self.problem_build_helper.substitude_variable(ret, 'X', 'xopt', self.op.optvars.n_vars)
        ret = self.problem_build_helper.substitude_variable(ret, 'Y', 'xopt', self.op.optvars.n_vars, self.test_op.optvars.idxs['Y'][0,0])
        target_output = \
"""    H[0] = (xopt[0]+xopt[0]);
    H[5] = (xopt[1]+xopt[1]);
    H[8] = (xopt[2]+xopt[2]);
    H[13] = (xopt[3]+xopt[3]);"""
        self.assertTrue(ret == target_output)


    def test_build_matrix(self):

        with self.subTest("Vector"):
            X = casadi.SX.sym("X", 1, 1)
            matrix = casadi.SX.sym("vector", 3, 1)
            matrix[0:2] = 0
            matrix[2] = X**2
            ret = self.problem_build_helper.build_matrix("vector", matrix, dense=True)
            target_output = \
"""    double vector_temporary1 = 0;
    vector[0,0] = vector_temporary1;
    vector[1,0] = vector_temporary1;
    vector[2,0] = sq(X);"""
            self.assertTrue(target_output == ret)

            ret = self.problem_build_helper.build_matrix("vector", matrix)
            target_output = \
"""    double vector_temporary1 = 0;
    vector[0] = vector_temporary1;
    vector[1] = vector_temporary1;
    vector[2] = sq(X);"""
            self.assertTrue(target_output == ret)

        with self.subTest("Matrix"):
            X = casadi.SX.sym("X", 1, 1)
            matrix = casadi.SX.sym("vector", 2, 2)
            matrix[0, 0] = 0
            matrix[1, 0] = 0
            matrix[0, 1] = 0
            matrix[1, 1] = X**2
            ret = self.problem_build_helper.build_matrix("matrix", matrix, dense=True)
            target_output = \
"""    double matrix_temporary1 = 0;
    matrix[0,0] = matrix_temporary1;
    matrix[0,1] = matrix_temporary1;
    matrix[1,0] = matrix_temporary1;
    matrix[1,1] = sq(X);"""
            self.assertTrue(ret == target_output)

            ret = self.problem_build_helper.build_matrix("matrix", matrix)
            target_output = \
"""    double matrix_temporary1 = 0;
    matrix[0] = matrix_temporary1;
    matrix[1] = matrix_temporary1;
    matrix[2] = matrix_temporary1;
    matrix[3] = sq(X);"""
            self.assertTrue(ret == target_output)

            ret = self.problem_build_helper.build_matrix("matrix", matrix, as_matrix=False)
            target_output = \
"""    double matrix_temporary1 = 0;
    matrix(0,0) = matrix_temporary1;
    matrix(1,0) = matrix_temporary1;
    matrix(0,1) = matrix_temporary1;
    matrix(1,1) = sq(X);"""
            self.assertTrue(ret == target_output)

            ret = self.problem_build_helper.build_matrix("matrix", matrix, as_matrix=False, dense=True)
            target_output = \
"""    double matrix_temporary1 = 0;
    matrix[0,0] = matrix_temporary1;
    matrix[0,1] = matrix_temporary1;
    matrix[1,0] = matrix_temporary1;
    matrix[1,1] = sq(X);"""
            self.assertTrue(ret == target_output)


if __name__ == '__main__':
    unittest.main()
