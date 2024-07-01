import casadi

from flat_om_model_importer import ModelParser

import numpy as np
import sys
sys.path.append("..")
sys.path.append("../helpers")
sys.path.append("../openmodelica_parser")
from optimizationproblem import OptimizationProblem
from discretize_model import mk2
from model_variables import ModelVariables
from parse_om_function_to_casadi import parse_om_function_to_casadi
import variables

def read_model(model_path):
    with open(model_path, "r") as f:
        model_text = f.read()
        model_text = model_text.replace(".", "_")
    return model_text



def create_op_variables(model_parser: ModelParser, model_inputs: [str], K: int, params_as_vars=False):
    model_inputs = [u.replace(".", "_") for u in model_inputs]
    op = OptimizationProblem()
    model_x = variables.Variables()
    model_u = variables.Variables()
    model_params = variables.Variables()
    for xopt in model_parser.variables:
        if xopt in model_inputs:
            op.optvars.register(xopt, [1, K-1])
            model_u.register(xopt)
            model_inputs.remove(xopt)
        else:
            op.optvars.register(xopt, [1, K])
            model_x.register(xopt)

    for param in model_parser.parameters:
        if params_as_vars:
            op.optvars.register(param)
        else:
            op.problem_parameters.register(param)
        model_params.register(param)

    if len(model_inputs) > 0:
        raise ValueError(f"Not all model inputs found: {model_inputs}")

    model_vars = ModelVariables(model_x, model_u, model_params)
    return op, model_vars


def create_op_with_om_model(model_path, model_inputs, dt:float, K:int, params_as_vars=False):
    model_text = read_model(model_path)
    model_parser = ModelParser(model_text)
    op, model_vars = create_op_variables(model_parser, model_inputs, K, params_as_vars)

    for ode in model_parser.odes:
        sites = ode.split(" = ")
        if 'der(' in sites[1]:
            sites = list(reversed(sites))

        ode_variable = sites[0].replace('der(', '').replace(")", "")
        ode_equation = sites[1]
        constr = mk2(ode_variable, ode_equation, op, model_vars, dt)

        op.constraints.register(sites[0], constr)

    X = op.optvars.variables_by_names(model_vars.X.names).reshape((-1,model_vars.X.n_vars)).T
    U = op.optvars.variables_by_names(model_vars.U.names).reshape((-1,model_vars.U.n_vars)).T
    if params_as_vars:
        Params = op.optvars.variables_by_names(model_vars.params.names).reshape((-1,model_vars.params.n_vars)).T
    else:
        Params = op.problem_parameters.variables_flat()

    for eq in model_parser.equations:
        [eq_lh, eq_rh] = eq.split(" = ")

        eq_rh_func = parse_om_function_to_casadi(model_vars, eq_rh)
        print(f"{eq_rh}")
        print(eq_rh_func(X[:,:-1], U, Params))

        eq_lh_func = parse_om_function_to_casadi(model_vars, eq_lh)
        print(f"{eq_lh}")
        print(eq_lh_func(X[:,:-1], U, Params))
        constraint = eq_lh_func(X[:,:-1], U, Params) - eq_rh_func(X[:,:-1], U, Params)
        op.constraints.register(eq, constraint)

    return op


