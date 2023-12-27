#!/usr/bin/env python3
import sys
sys.path.append("..")
from variables import Variables
from optimizationproblem import OptimizationProblem
import cpp_struct_functions


def build_osstreams(op:OptimizationProblem) -> str:
    ret =  cpp_struct_functions.cpp_struct_osstream(op.scenario_parameters, "scenario_parameter")
    ret += cpp_struct_functions.cpp_struct_osstream(op.problem_parameters, "problem_parameter")
    ret += cpp_struct_functions.cpp_struct_osstream(op.optvars, "optimized_variable")
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
