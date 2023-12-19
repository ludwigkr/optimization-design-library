#!/usr/bin/env python3
import sys
sys.path.append("..")
from variables import Variables
from optimizationproblem import OptimizationProblem
import cpp_struct_functions
from substitute_variables import substitute_variable, substitute_variable_in_struct
from scalar_expression_parser import parse_scalar_casadi_expression

def build_osstreams(op:OptimizationProblem) -> str:
    ret =  cpp_struct_functions.cpp_struct_osstream("scenario_parameter", op.scenario_parameters)
    ret += cpp_struct_functions.cpp_struct_osstream("problem_parameter", op.problem_parameters)
    ret += cpp_struct_functions.cpp_struct_osstream("optimized_variable", op.optvars)
    return ret


def build_mappers(op:OptimizationProblem) -> str:
    ret = "std::tuple<std::map<std::string, size_t>, std::map<std::string, size_t>, std::map<std::string, size_t>> mappers(){\n"
    ret += "    std::map<std::string, size_t> map_scenario;\n"
    ret += "    std::map<std::string, size_t> map_prob_param;\n"
    ret += "    std::map<std::string, size_t> map_xopt;\n\n"

    def variable_offsets(map_name: str, struct_name: str, var: Variables) -> str:
        ret = ""
        for name in var.names:
            ret += f'    {map_name}["{name}"] = offsetof({struct_name}, {name});\n'
        ret += "\n"
        return ret

    ret += variable_offsets("map_scenario", "scenario_parameter", op.scenario_parameters)
    ret += variable_offsets("map_prob_param", "problem_parameter", op.problem_parameters)
    ret += variable_offsets("map_xopt", "optimized_variable", op.optvars)

    ret += "    return std::tuple(map_scenario, map_prob_param, map_xopt);\n"
    ret += "};"
    return ret

def substitude_optimization_variables(exp: str, op: OptimizationProblem, prob_param_as_struct=False) -> str:
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

def optimizer_objective_expression(op: OptimizationProblem, objective_variable_name: str):
    exp = parse_scalar_casadi_expression(objective_variable_name, op.objective)
    exp = substitude_optimization_variables(exp, op, prob_param_as_struct=True)
    return exp

def build_operators(op:OptimizationProblem) -> str:
    ret = "optimized_variable operator-(const optimized_variable& left, const optimized_variable& right) {\n"
    ret += "    optimized_variable ret;\n"
    for name in op.optvars.names:
            ret += f'    ret.{name} = left.{name} - right.{name};\n'
    ret += "    return ret;\n"
    ret += "};"

    return ret