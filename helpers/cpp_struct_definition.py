#!/usr/bin/env python3
import sys
sys.path.append("..")
from variables import Variables
from parser_common import floating_type, vector_type, matrix_type

def cpp_struct_definition_name(name: str) -> str:
    return "struct " + name + "{\n"

def cpp_struct_definition_entries(var: Variables) -> str:
    ret = ""
    for vi, v in enumerate(var.variables):
        if v.size1() == 1 and v.size2() == 1:
            ret += f"    {floating_type} " + var.names[vi] + ";\n"
        elif v.size1() > 1 and v.size2() > 1:
            ret += f"    {matrix_type} " + var.names[vi] + ";\n"
        else:
            ret += f"    {vector_type} " + var.names[vi] + ";\n"

    return ret

def cpp_struct_definition_constructors(name: str, var: Variables) -> str:
    ret = ""
    if len(var.variables) > 0:
        ret += "\n    " + name + "("
        for vi, v in enumerate(var.variables):
            if v.size1() == 1 and v.size2() == 1:
                ret += f"{floating_type} _{var.names[vi]}, "
            elif v.size1() > 1 and v.size2() > 1:
                ret += f"{matrix_type} _{var.names[vi]}, "
            else:
                ret += f"{vector_type} _{var.names[vi]}, "
            if ret[-2:] == ', ':
                ret = ret[:-2]
            ret += "):\n"

        for vi, v in enumerate(var.variables):
            ret += "        " + var.names[vi] + "(_" + var.names[vi] + "),\n"
        ret = ret[:-2]
        ret += "{}\n\n    "
        ret += name+"(){\n"
        for vi, v in enumerate(var.variables):
            if v.size1() == 1 and v.size2() == 1:
                # variable_structure += "          float _" + var.names[vi] + ", "
                pass
            elif v.size1() > 1 and v.size2() > 1:
                ret += f"          {var.names[vi]} = {matrix_type}({v.size(1)},{v.size(2)});\n"
            else:
                ret += f"          {var.names[vi]} = {vector_type}({v.size(1)*v.size(2)});\n"
            ret += "}\n"

    return ret

def cpp_struct_definition_norm_function(var: Variables):
        ret = f"    {floating_type} norm() " + "{\n"
        ret += f"        {floating_type} ret = 0;" + "\n"
        for vi, v in enumerate(var.variables):
            if v.size1() == 1 and v.size2() == 1:
                ret += f"        ret += powf({var.names[vi]}, 2);" + "\n"
            elif v.size1() > 1 and v.size2() > 1:
                ret += f"        ret += {var.names[vi]}.cwiseProduct({var.names[vi]}).sum();" + "\n"
            else:
                ret += f"        ret += {var.names[vi]}.transpose() * {var.names[vi]};" + "\n"
        ret += "        return sqrt(ret);\n"
        ret += "    }\n"

        return ret

def cpp_struct_definition_end():
    return "};"


def cpp_struct_definition(name: str, var: Variables) -> str:
    ret = cpp_struct_definition_name(name)
    ret += cpp_struct_definition_entries(var)
    ret += cpp_struct_definition_constructors(name, var)
    ret += cpp_struct_definition_norm_function(var)
    ret += cpp_struct_definition_end()
    return ret
