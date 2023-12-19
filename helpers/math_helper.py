#!/usr/bin/env python3
import casadi
import numpy as np

def symetric_based_on_numeric(mat: casadi.SX, vars: [casadi.SX]) -> bool:
    f = casadi.Function('mat', vars, [mat])
    f_transposed = casadi.Function('mat', vars, [mat.T])

    for i in range(10):
        sample = []
        for var in vars:
            if type(var) != list:
                sample_var = 2e3 * np.random.rand(var.size()[0], var.size()[1]) - 1e3
                sample.append(sample_var)
            else:
                sample.append([])

        if len(sample) == 1:
            sample = sample[0]

        check1 = f(sample[0], sample[1], sample[2])
        check2 = f_transposed(sample[0], sample[1], sample[2])
        check = np.array(check1) - np.array(check2)
        check = np.linalg.norm(check)

        if check > 1e-4:
            return False

    return True

def index_is_upper_triangular(row_index:int, column_index:int, has_lower_triangular_shape: True) -> bool:
    return column_index > row_index and has_lower_triangular_shape
