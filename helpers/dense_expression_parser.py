#!/usr/bin/env python3
import sys
import casadi
import logging
from parser_common import temporary_postfix, build_expression_definitions

def expression_to_dense_string_elements(expression: casadi.SX) -> str:
    tmp_file = '/tmp/opti_design_lib'
    with open(tmp_file,'wt') as sys.stdout:
        expression.print_dense()
    sys.stdout = sys.__stdout__
    with open(tmp_file, "r") as f:
        ret = f.read()
    with open(tmp_file, "w"):
        pass
    ret = ret.split(',')
    return ret

def filter_string_elements(string_elements: [str]):
    definition_elements = [e for e in string_elements if e[0] == '@' or (e[0:2]==' @' and ']' not in e)]
    value_elements = [e for e in string_elements if (e[0] != '@' and e[0:2] != ' @') or ']' in e]
    return definition_elements, value_elements

def build_dense_expression_values(name, vals: [str], one_dimensional):
    ret = ''
    row = 0
    column = 0
    warning_given = False
    temp_name = name + temporary_postfix
    for val in vals:

        if not warning_given and one_dimensional and row>0:
           logging.getLogger(__name__).warning("Vector requested but 2D matrix given. Return column-wise vectorized matrix.")
           warning_given = True

        original_val = val
        val = val.replace('[','').replace(']','').replace('\n','').replace(' ', '').replace('00', '0')

        if one_dimensional:
            ret += f"{name}[{column}] = {val};\n"
        else:
            ret += f"{name}[{row},{column}] = {val};\n"

        column += 1

        if ']' in original_val:
            if not one_dimensional:
                column = 0
            row += 1

    ret = ret.replace("@", temp_name)
    return ret

def parse_dense_casadi_expression(name: str, expression: casadi.SX, one_dimensional = False) -> str:
    if type(expression) != casadi.SX:
        expression = casadi.SX(expression)

    if expression.size1() == 0 or expression.size2() == 0:
        return ""

    string_elements = expression_to_dense_string_elements(expression)
    definition_elements, value_elements = filter_string_elements(string_elements)
    ret = build_expression_definitions(name, definition_elements)
    ret += build_dense_expression_values(name, value_elements, one_dimensional)
    return ret
