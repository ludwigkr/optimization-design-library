#!/usr/bin/env python3
import sys
sys.path.append("..")
from variables import Variables

def compare_cpp_sruct(type_name: str, var: Variables) -> str:
    ret = f"{type_name} operator-(const {type_name}& left, const {type_name}& right) "
    ret += "{\n"
    ret += f"    {type_name} ret;"
    ret += "\n"
    for name in var.names:
            ret += f'    ret.{name} = left.{name} - right.{name};\n'
    ret += "    return ret;\n"
    ret += "};"
    return ret

def cpp_struct_osstream(vars_name: str, vars: Variables):
    ret = f"std::ostream& operator<<(std::ostream& os, const {vars_name}& s) " + "{\n"
    ret += '   return os << "{'
    for name in vars.names:
        if len(vars.idxs[name]) > 1:
            ret += f' {name}: " << s.{name}.transpose() << ", '
        else:
            ret += f' {name}: " << s.{name} << ", '
        if len(vars.names) > 0:
            ret = ret[:-3]
        ret += ' "'
    ret += ' }";\n'
    ret += "};\n\n"
    return ret

def assign_vector_values_to_struct_entries(vector_name: str, struct_name: str, vars: Variables, pointer=False):
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
