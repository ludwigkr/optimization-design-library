from optimizationproblem import OptimizationProblem, Variables

import os
import sys
import casadi
import numpy as np
from pathlib import Path

local_folder_path = os.path.dirname(__file__)
sys.path.append(local_folder_path + "/casadi_parser")


def definition_export(op: OptimizationProblem, custome_defines="", trajectory_parameter=None):
    header_content = "#pragma once\n"
    header_content += '#define ' + op.name.upper() + '_VERSION "' + str(op.version) + '"\n'
    header_content += '#define N_OPTVARS ' + str(op.optvars.n_vars) + '\n'
    header_content += '#define N_CONSTRAINTS ' + str(op.constraints.n_constraints) + '\n'
    header_content += custome_defines
    header_content += "\n"

    header_content += "enum optvar_idx {\n"
    for j, idxs_key in enumerate(op.optvars.idxs):
        name = op.optvars.names[j]
        idxs = op.optvars.idxs[idxs_key]
        if len(idxs) == 1:
            header_content += "    " + name + " = " + str(op.optvars.idxs[idxs_key][0, 0]) + ",\n"
        else:
            header_content += "    " + name + "_first = " + str(op.optvars.idxs[idxs_key][0, 0]) + ",\n"
            header_content += "    " + name + "_last = "  + str(op.optvars.idxs[idxs_key][-1, -1]) + ",\n"
    header_content += "};\n"
    header_content += "\n"

    header_content += "enum inequality_constraint_idx {\n"
    for j, idxs_key in enumerate(op.constraints.idxs):
        name = idxs_key
        idxs = op.constraints.idxs[idxs_key]
        if len(idxs) == 1:
            header_content += "    " + name + " = " + str(op.constraints.idxs[idxs_key][0]) + ",\n"
        else:
            header_content += "    " + name + "_first = " + str(op.constraints.idxs[idxs_key][0]) + ",\n"
            header_content += "    " + name + "_last = "  + str(op.constraints.idxs[idxs_key][-1]) + ",\n"
    header_content += "};\n"
    header_content += "\n"

    if trajectory_parameter:
        header_content += "enum trjactory_parameter {\n"
        for parameter in trajectory_parameter:
            header_content += "    " + str(parameter) + " = " + str(trajectory_parameter[parameter]) + ",\n"
        header_content += "};\n"


    with open(Path("./" + op.name + "_index.h").expanduser(), "w") as f:
        f.write(header_content)

def build_solver(op: OptimizationProblem, opts):

    assert(op.objective is not None)
    assert(not op.fn_initial_guess.function.is_null())
    assert(not op.fn_lbx.function.is_null())
    assert(not op.fn_ubx.function.is_null())
    assert(not op.fn_lbg.function.is_null())
    assert(not op.fn_ubg.function.is_null())
    op.fn_params.build('fn_problem_parameters', op.problem_parameter, op.scenario_parameter, op.problem_parameter.variables_flat())
    # assert(not op.fn_initial_guess.is_null())

    solver = casadi.nlpsol('solver', opts["optimizer"], {'x': op.optvars.variables_flat(), 'p': op.problem_parameter.variables_flat(), 'f': op.objective, 'g': op.constraints.equations_flat()}, opts["options"])
    solver.generate_dependencies(op.name + '_optimizer.cpp', {'with_header': False, 'cpp': False})
    os.system("gcc -fPIC -shared -O3 " + op.name + "_optimizer.cpp -o " + op.name + "_optimizer.so")

    definition_export(op, op.exported_defines.code, op.trajectory_parameter.parameter)

    return solver

def run(solver, op: OptimizationProblem, scenario_parameter: Variables, parameters: Variables=None):
    initial_guess = op.fn_initial_guess.call(parameters, scenario_parameter)
    lb = op.fn_lbx.call(parameters, scenario_parameter)
    ub = op.fn_ubx.call(parameters, scenario_parameter)
    lbg = op.fn_lbg.call(parameters, scenario_parameter)
    ubg = op.fn_ubg.call(parameters, scenario_parameter)

    if parameters is not None:
        result = solver(x0=initial_guess, p=parameters, lbg=lbg, ubg=ubg, lbx=lb, ubx=ub)
    else:
        result = solver(x0=initial_guess, lbg=lbg, ubg=ubg, lbx=lb, ubx=ub)

    return result

def float2string(x):
    return str(f'{x:.2g}')


def formulation(op: OptimizationProblem, scenario_parameter, problem_parameter, result=None):
    init_guess = op.fn_initial_guess.call(problem_parameter, scenario_parameter)
    lb = op.fn_lbx.call(problem_parameter, scenario_parameter)
    ub = op.fn_ubx.call(problem_parameter, scenario_parameter)
    lbg = op.fn_lbg.call(problem_parameter, scenario_parameter)
    ubg = op.fn_ubg.call(problem_parameter, scenario_parameter)

    variable_table = "| idx | optimization_variables | initial guess |   lbx |  ubx | optimized_values | lam_x |\n"
    variable_table +="|-----|------------------------|---------------|-------|------|------------------|-------|\n"
    for i in range(int(op.optvars.n_vars)):
        for j in op.optvars.idxs:
            if i in op.optvars.idxs[j]:
                break
        block_indicator = int(i - casadi.reshape(op.optvars.idxs[j][0], 1, -1)[0])
        variable_table += "| " + str(i) + " | " + j + "_" + str(block_indicator) + " | " + float2string(float(init_guess[i])) + " | " + float2string(float(lb[i])) + " | " + float2string(float(ub[i])) + " | "
        if result is None:
            variable_table += " |  |\n"
        else:
            variable_table += float2string(float(np.array(result['x'][i]))) + " | " + float2string(float(np.array(result['lam_x'][i]))) + " |\n"

    constraint_table = "| idx | name | constraint | g | lbg | ubg | g_opt | lam_g |\n"
    constraint_table +="|-----|------|------------|---|-----|-----|-------|-------|\n"
    idx_constrait_i = 0
    idx_constraint_block = 0
    g0 = np.array(op.equation_values(init_guess, problem_parameter))
    gopt = np.array(op.equation_values(result['x'], problem_parameter))
    for constraint_block_name in op.constraints.idxs:
        for idx_subconstraint in list(op.constraints.idxs[constraint_block_name]):
            local_idx_constraint = idx_constrait_i - op.constraints.idxs[constraint_block_name][0]
            constraint_table += "| " + str(idx_constrait_i) + " | " + constraint_block_name + "_" + str(local_idx_constraint) + " | " \
                + str(op.constraints.equations[idx_constraint_block][local_idx_constraint]) + " | " \
                + float2string(float(g0[idx_constrait_i])) + " | "\
                + float2string(float(lbg[idx_constrait_i])) + " | " + float2string(float(ubg[idx_constrait_i])) + " |"
            if result is None:
                constraint_table += "  |  |\n"
            else:
                constraint_table += float2string(float(gopt[idx_subconstraint])) + " | "
                constraint_table += float2string(float(np.array(result['lam_g'][idx_subconstraint]))) + " |\n"
            idx_constrait_i += 1
        idx_constraint_block += 1

    formulation = "#+title: " + op.name + " (version " + str(op.version) + ")"
    formulation += "\n\n"
    formulation += "*Objective:*\n"
    formulation += str(op.objective)
    formulation += "\n\n"
    formulation += "*Box constraints:*\n"
    formulation += variable_table
    formulation += "\n\n"
    formulation += "*Inequality constraints:*\n"
    formulation += constraint_table

    # print(formulation)
    return formulation

def write_formulation(op: OptimizationProblem, scenario_parameter, parameter=None, result=None):
    formulation_text = formulation(op, scenario_parameter, parameter, result)

    file = "ocp_" + op.name + ".org"
    with open(file, "w") as f:
        f.write(formulation_text)