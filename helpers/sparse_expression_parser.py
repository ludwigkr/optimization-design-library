#!/usr/bin/env python3
import sys
import casadi
from dense_expression_parser import parse_dense_casadi_expression
from math_helper import index_is_upper_triangular

class SparseParserConfiguration():
    def __init__(self):
        self.target_optimizer = "ipopt"

sparse_config = SparseParserConfiguration()

def SX_sparse_str(mat: casadi.SX) -> str:
    tmp_file = '/tmp/opti_design_lib'
    with open(tmp_file,'wt') as sys.stdout:
    # sys.stdout = open(tmp_file,'wt')
        mat.print_sparse(False)
    sys.stdout = sys.__stdout__
    with open(tmp_file, "r") as f:
        ret = f.read()
    with open(tmp_file, "w"):
        pass
    ret = ret.replace(' ', '')
    ret = ret.split('\n')
    return ret

def build_ipopt_index(expression: casadi.SX, has_lower_triangular_shape=False):
    ret = ""
    smat = SX_sparse_str(expression)
    value_lines = [e for e in smat if e[0] == '(']
    line_index = 0
    for l, line in enumerate(value_lines):
        index_str = line.split("->")[0].replace("(", "").replace(")", "").split(",")
        row = int(index_str[0])
        column = int(index_str[1])
        if not is_structual_zero_entry(expression[row,column], has_lower_triangular_shape, row, column):
            ret += f"iRow[{line_index}] = {row};\n"
            ret += f"jCol[{line_index}] = {column};\n"
            line_index += 1
    return ret


def is_structual_zero_entry(expression: casadi.SX, has_lower_triangular_shape: bool, row_index: int, column_index: int):
    is_zero = str(expression) == "0" or str(expression) == "00"
    tmp = index_is_upper_triangular(row_index, column_index, has_lower_triangular_shape)
    return is_zero or tmp

def count_structual_nonzero_entries(expression: casadi.SX, has_lower_triangular_shape: bool):
    n_nonzero = 0
    for row in range(expression.size(1)):
        for col in range(expression.size(2)):
            if not is_structual_zero_entry(expression[row,col], has_lower_triangular_shape, row, col):
                n_nonzero += 1

    return n_nonzero


def matrix_expression_to_ipopt_value_vector(expression: casadi.SX, has_lower_triangular_shape: bool):
    nnz = count_structual_nonzero_entries(expression, has_lower_triangular_shape)
    ipopt_value_vector = casadi.SX.sym('tmp', nnz, 1)
    idx = 0
    for col in range(expression.size(2)): # Important to iterate first through cols and then rows due to the expected shape of the matrix
        for row in range(expression.size(1)):
            if not is_structual_zero_entry(expression[row,col], has_lower_triangular_shape, row, col):
                ipopt_value_vector[idx] = expression[row,col]
                idx += 1

    return ipopt_value_vector


def build_ipopt_values(expression: casadi.SX, has_lower_triangular_shape=False):
    expression = matrix_expression_to_ipopt_value_vector(expression, has_lower_triangular_shape)
    ret = parse_dense_casadi_expression("values", expression, one_dimensional=True)
    return ret

def parse_sparse_casadi_expression(name: str, exp: casadi.SX, one_dimensional = False, has_lower_triangular_shape=False) -> str:
    if sparse_config.target_optimizer == "ipopt":
        index = build_ipopt_index(exp, has_lower_triangular_shape)
        values = build_ipopt_values(exp, has_lower_triangular_shape)

    return index, values
