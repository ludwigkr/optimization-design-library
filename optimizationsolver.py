from optimizationproblem import OptimizationProblem, Variables

import json
import os
import sys
import casadi
import numpy as np
from pathlib import Path

local_folder_path = os.path.dirname(__file__)
sys.path.append(local_folder_path + "/casadi_parser")

def build_solver(op: OptimizationProblem, opts):
    forbidden_variables = ['lam', 'x', 'xopt', 'param']

    assert(op.objective is not None)
    assert(not op.fn_initial_guess.function.is_null())
    assert(not op.fn_lbx.function.is_null())
    assert(not op.fn_ubx.function.is_null())
    assert(not op.fn_lbg.function.is_null())
    assert(not op.fn_ubg.function.is_null())
    for scenario in op.scenario_parameters.names:
        assert scenario not in forbidden_variables, f"{scenario} in {forbidden_variables =}, please change your variable name."

    for prob_param in op.problem_parameters.names:
        assert prob_param not in forbidden_variables, f"{prob_param} in {forbidden_variables =}, please change your variable name."

    for xopt in op.optvars.names:
        assert xopt not in forbidden_variables, f"{xopt} in {forbidden_variables =}, please change your variable name."

    op.fn_params.build('fn_problem_parameters', op.problem_parameters, op.scenario_parameters, op.problem_parameters.variables_flat())
    # assert(not op.fn_initial_guess.is_null())

    solver = casadi.nlpsol('solver', opts["optimizer"], {'x': op.optvars.variables_flat(), 'p': op.problem_parameters.variables_flat(), 'f': op.objective, 'g': op.constraints.equations_flat()}, opts["options"])
    # solver.generate_dependencies(op.name + '_optimizer.cpp', {'with_header': True, 'cpp': True})
    # os.system("gcc -fPIC -shared -O3 " + op.name + "_optimizer.cpp -o " + op.name + "_optimizer.so")
    # definition_export(op, op.exported_defines.code)

    return solver

def run(solver, op: OptimizationProblem, scenario_parameters: Variables, parameters: Variables=None):
    initial_guess = op.fn_initial_guess.call(parameters, scenario_parameters)
    lb = op.fn_lbx.call(parameters, scenario_parameters)
    ub = op.fn_ubx.call(parameters, scenario_parameters)
    lbg = op.fn_lbg.call(parameters, scenario_parameters)
    ubg = op.fn_ubg.call(parameters, scenario_parameters)

    if parameters is not None:
        result = solver(x0=initial_guess, p=parameters, lbg=lbg, ubg=ubg, lbx=lb, ubx=ub)
    else:
        result = solver(x0=initial_guess, lbg=lbg, ubg=ubg, lbx=lb, ubx=ub)

    return result

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


class TestCaseExporter():
    def __init__(self):
        self.export = '{"cases":['
        self.n = 0

    def add_case(self, ocp: OptimizationProblem, scenario, prob_param, result) -> str:
        if self.n > 0:
            self.export += ","
        ret = '{"scenario": ' + self.tojson(ocp.scenario_parameters, ocp.scenario_parameters.packed(scenario)) + ','
        ret += '"prob_param": ' + self.tojson(ocp.problem_parameters, ocp.problem_parameters.packed(prob_param)) + ','
        ret += '"xopt": ' + self.tojson(ocp.optvars, ocp.optvars.packed(result['x'])) + '}'
        self.export += ret
        self.n += 1

        return ret

    def value_to_json(self, name: str, val: casadi.DM) -> str:
        is_matrix = val.shape[0] > 1 and val.shape[1] > 1
        is_scalar = val.shape[0] == 1 and val.shape[1] == 1
        if is_matrix:
            return f'"{name}": {val},'
        elif is_scalar:
            return f'"{name}": {val[0]},'
        else:
            return f'"{name}": {list(np.array(val).reshape((-1)))},'

    
    def tojson(self, var:Variables, val: casadi.DM) -> str:
        ret = "{"
        if len(var.names) == 0:
            ret += ","
        elif len(var.names) == 1:
            ret += self.value_to_json(var.names[0], val)
        elif len(var.names) > 1:
            for i, name in enumerate(var.names):
                ret += self.value_to_json(name, val[i])
        ret = ret[:-1]
        ret += "}"
        return ret

    def save(self, path: str=None):
        if path == None:
            path = "./test-cases.json"

        folder = os.path.dirname(path)
        if not os.path.exists(folder):
            os.makedirs(folder)

        self.export += "]}"
        self.export = self.export.replace(" 00", " 0").replace("[00", "[0").replace("\n","")
        print(self.export)

        with open(path, "w") as f:
            f.write(json.dumps(json.loads(self.export), indent=2))
            # f.write(self.export)
