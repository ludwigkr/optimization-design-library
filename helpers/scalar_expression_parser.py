
#!/usr/bin/env python3
import casadi
from dense_expression_parser import parse_dense_casadi_expression

def remove_matrix_information_lhs(exp: str) -> str:
    lines = exp.split("\n")
    exp_split = lines[-2].split("=")
    val_name = exp_split[0].split("[")[0].replace(" ", "")
    lines[-2] = val_name + " =" + exp_split[1]
    exp = "\n".join(lines)
    return exp

def parse_scalar_casadi_expression(name: str, exp: casadi.SX) -> str:
    ret = parse_dense_casadi_expression(name, exp)
    ret = remove_matrix_information_lhs(ret)
    return ret
