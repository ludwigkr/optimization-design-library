import casadi

from model_parser import ModelParser

import numpy as np
import sys
sys.path.append("..")
sys.path.append("../helpers")
sys.path.append("../openmodelica_parser")
from optimizationproblem import OptimizationProblem
from discretize_model import mk2
from parse_to_casadi_function import parse_to_casadi_function
from read_model import read_model


def create_optimizaiton_problem_with_variables(model_parser: ModelParser, K: int, params_as_vars=False):
    op = OptimizationProblem()
    for state in model_parser.variables.states:
        op.optvars.register(state, [1, K])

    for actuator in model_parser.variables.inputs:
        op.optvars.register(actuator, [1, K-1])

    for param in model_parser.variables.parameters:
        if params_as_vars:
            op.optvars.register(param)
        else:
            op.problem_parameters.register(param)

    return op

def add_odes_constraints(op: OptimizationProblem, model_parser: ModelParser, dt, params_as_vars: bool):
    for ode in model_parser.equations.odes:
        sites = ode.split(" = ")
        if 'der(' in sites[1]:
            sites = list(reversed(sites))

        ode_variable = sites[0].replace('der(', '').replace(")", "")
        ode_equation = sites[1]
        constr = mk2(ode_variable, ode_equation, op, model_parser, dt, params_as_vars=params_as_vars)

        op.constraints.register(sites[0], constr)

    return op

def add_constraint_equations(op: OptimizationProblem, model_parser: ModelParser, params_as_vars: bool):
    X = op.optvars.variables_by_names(model_parser.variables.states.names)
    if model_parser.variables.states.n_vars > 0:
        X = X.reshape((-1,model_parser.variables.states.n_vars)).T

    U = op.optvars.variables_by_names(model_parser.variables.inputs.names)
    if model_parser.variables.inputs.n_vars > 0:
        U = U.reshape((-1,model_parser.variables.inputs.n_vars)).T

    if params_as_vars:
        Params = op.optvars.variables_by_names(model_parser.variables.parameters.names).reshape((-1,model_parser.variables.parameters.n_vars)).T
    else:
        Params = op.problem_parameters.variables_flat()

    for eq in model_parser.equations.constraints:
        [eq_lh, eq_rh] = eq.split(" = ")

        eq_rh_func = parse_to_casadi_function(model_parser.variables, eq_rh)
        eq_lh_func = parse_to_casadi_function(model_parser.variables, eq_lh)
        constraint = eq_lh_func(X[:,:-1], U, Params) - eq_rh_func(X[:,:-1], U, Params)
        op.constraints.register(eq, constraint)

    return op


def optimization_problem_from_modelica_model(model_path: str, model_inputs: [str], dt:float, K:int, params_as_vars=False):
    model_text = read_model(model_path)
    model_parser = ModelParser(model_text)
    model_parser.variables.inputs_are(model_inputs)
    model_parser.variables.outputs_are_states()

    op = create_optimizaiton_problem_with_variables(model_parser, K, params_as_vars)
    
    model_parser.variables.convert_variables_to_symbolics()
    op = add_odes_constraints(op, model_parser, dt, params_as_vars)
    op = add_constraint_equations(op, model_parser, params_as_vars)
    return op


