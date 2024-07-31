import sys
sys.path.append("..")

import casadi
import numpy as np
from optimizationproblem import OptimizationProblem

def float2string(x):
    return str(f'{x:.2g}')

def core_formulation(op: OptimizationProblem):
    variable_table = "| idx | optimization_variables |\n"
    variable_table +="|-----|------------------------|\n"
    for i in range(int(op.optvars.n_vars)):
        for j in op.optvars.idxs:
            if i in op.optvars.idxs[j]:
                break
        block_indicator = int(i - casadi.reshape(op.optvars.idxs[j][0], 1, -1)[0])
        variable_table += "| " + str(i) + " | " + j + "_" + str(block_indicator) + " |\n"

    constraint_table = "| idx | name | constraint |\n"
    constraint_table +="|-----|------|------------|\n"
    idx_constrait_i = 0
    idx_constraint_block = 0
    for constraint_block_name in op.constraints.idxs:
        for idx_subconstraint in list(op.constraints.idxs[constraint_block_name]):
            local_idx_constraint = idx_constrait_i - op.constraints.idxs[constraint_block_name][0]
            constraint_table += "| " + str(idx_constrait_i) + " | " + constraint_block_name + "_" + str(local_idx_constraint) + " | " \
                + str(op.constraints.equations[idx_constraint_block][local_idx_constraint]) + " |\n"
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

    return formulation


def formulation(op: OptimizationProblem, scenario_parameters, problem_parameters, result=None):
    init_guess = op.fn_initial_guess.call(problem_parameters, scenario_parameters)
    lb = op.fn_lbx.call(problem_parameters, scenario_parameters)
    ub = op.fn_ubx.call(problem_parameters, scenario_parameters)
    lbg = op.fn_lbg.call(problem_parameters, scenario_parameters)
    ubg = op.fn_ubg.call(problem_parameters, scenario_parameters)

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
    g0 = np.array(op.equation_values(init_guess, problem_parameters))
    gopt = np.array(op.equation_values(result['x'], problem_parameters))
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

def write_formulation(op: OptimizationProblem, scenario_parameters, parameters=None, result=None):
    formulation_text = formulation(op, scenario_parameters, parameters, result)

    file = "ocp_" + op.name + ".org"
    with open(file, "w") as f:
        f.write(formulation_text)
