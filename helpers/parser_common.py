#!/usr/bin/env python3

floating_type = "float"
vector_type = "Eigen::VectorXd"
matrix_type = "Eigen::MatrixXd"
temporary_postfix = "_temporary"

def build_expression_definitions(name, defs: [str]) -> str:
    ret = ""
    tmp_name = name + temporary_postfix
    for i, _def in enumerate(defs):
        value = _def.split('=')[-1]
        value = value.replace('@', tmp_name)
        ret += f'{floating_type} {tmp_name + str(i+1)} = {value};' + "\n"
    return ret

def indent_lines(lines, except_first_line=True):
    is_str = False
    if type(lines) == str:
        is_str = True
        lines = lines.split("\n")

    if lines[-1] == '':
        del(lines[-1])

    first_line = 0
    if except_first_line:
        first_line = 1

    for i in range(first_line, len(lines)):
        lines[i] = f"    {lines[i]}"

    if is_str:
        lines = "\n".join(lines)

    return lines
