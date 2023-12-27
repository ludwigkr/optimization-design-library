#!/usr/bin/env python3

def class_name(name: str, quadratic_optimier=False) -> str:
    name = name.replace("_", " ")
    name = name.title()
    name = name.replace(" ", "")
    if quadratic_optimier:
        name = name + "QuadraticOptimizer"
    return name




def build_struct_of_variable(self, struct_name: str, vars: Variables, vector_name='x', pointer=False):
    connector = "."
    if pointer:
        connector = "->"
        ret = ""
    idx = 0
    for n, name in enumerate(vars.names):
        if vars.variables[n].size(1)*vars.variables[n].size(2) == 1:
                ret += f"    {struct_name}{connector}{name} = {vector_name}[{idx}];\n"
                idx += 1
        else:
            if vars.variables[n].size(1) == 1 or vars.variables[n].size(2) == 1:
                if vars.variables[n].size(1) == 1:
                    vars.variables[n] = vars.variables[n].T
                    for v in range(vars.variables[n].size(1)):
                    ret += f"    {struct_name}{connector}{name}[{v}] = {vector_name}[{idx}];\n"
                    idx += 1
            else:
                for c in range(vars.variables[n].size(2)):
                    for r in range(vars.variables[n].size(1)):
                        ret += f"    {struct_name}{connector}{name}({r}, {c}) = {vector_name}[{idx}];\n"
                        idx += 1
    return ret
    def build_operators(self, op:OptimizationProblem) -> str:
    ret = "optimized_variable operator-(const optimized_variable& left, const optimized_variable& right) {\n"
    ret += "    optimized_variable ret;\n"
for name in op.optvars.names:ret += f'    ret.{name} = left.{name} - right.{name};\n'ret += "    return ret;\n"ret += "};"return ret
