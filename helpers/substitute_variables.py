#!/usr/bin/env python3
import sys

sys.path.append("..")

import re
import numpy as np

from variables import Variables
from optimizationproblem import OptimizationProblem

def substitute_variable(exp: str, old_name: str, new_name: str, N: int, index_offset=0) -> str:
    if N == 1:
        search_pattern = "(?!_\w+)" + old_name + "(?!_\w+)"
        replace_pattern = new_name + "[" + str(index_offset) + "]"
        exp = re.sub(search_pattern, replace_pattern, exp)

    else:
        for n in reversed(range(N)):
            search_pattern = "(?!_\w+)" + old_name + "_" + str(n)+ "(?!_\w+)"
            replace_pattern = new_name + "[" + str(n + index_offset) + "]"
            exp = re.sub(search_pattern, replace_pattern, exp)

    return exp

def replace_pattern_for_substitute_variable_in_struct(struct_name: str, link_symbol: str, var: str, vars: Variables, n: int)->str:
    vars_idx = vars.idxs[var]
    var_is_matrix = np.array(vars_idx).shape[0] > 1 and np.array(vars_idx).shape[1] > 1
    if var_is_matrix:
        var_idx = np.where(vars_idx == n)
        var_idx = np.array(var_idx).reshape([-1]).tolist()
        replace_pattern = f"{struct_name}{link_symbol}{var}({int(var_idx[0])},{int(var_idx[1])})"
    else:
        replace_pattern = struct_name + link_symbol + var + "[" + str(n) + "]"
    return replace_pattern


def substitute_variable_in_struct(exp: str, sturct_name: str, link_symbol: str, vars: Variables) -> str:
    for v, var in enumerate(vars.names):
        N = vars.variables[v].size1() * vars.variables[v].size2()
        if N > 1:
            for n in reversed(range(N)):
                search_pattern = "(?!_\w+)" + var + "_" + str(n)+ "(?!_\w+)"
                var_idx = vars.idxs[var][0, 0] + n
                replace_pattern = replace_pattern_for_substitute_variable_in_struct(sturct_name, link_symbol, var, vars, var_idx)
                exp = re.sub(search_pattern, replace_pattern, exp)
        else:
            search_pattern = "(?!_\w+)" + var + "(?!_\w+)"
            replace_pattern = sturct_name + link_symbol + var
            exp = re.sub(search_pattern, replace_pattern, exp)

    return exp

def substitute_variables(exp: str, op: OptimizationProblem, prob_param_as_struct=False) -> str:

    ret = exp
    for optvar_name in op.optvars.names:
        ret = substitute_variable(ret, optvar_name, 'xopt', op.optvars.idxs[optvar_name].size, op.optvars.idxs[optvar_name][0,0])

    if prob_param_as_struct:
        ret = substitute_variable_in_struct(ret, "prob_param", "->", op.problem_parameters)
    else:
        for param_name in op.problem_parameters.names:
            ret = substitute_variable(ret, param_name, 'param', op.problem_parameters.idxs[param_name].size, op.problem_parameters.idxs[param_name][0,0])

    ret = substitute_variable(ret, 'lamg', 'lamg', op.constraints.n_constraints)
    ret = substitute_variable_in_struct(ret, 'scenario', '->', op.scenario_parameters)
    return ret
