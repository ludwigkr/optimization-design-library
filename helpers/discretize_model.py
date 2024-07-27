import casadi
from optimizationproblem import OptimizationProblem
from model_parser import ModelParser
from parse_to_casadi_function import parse_to_casadi_function


def prepare_variables(op: OptimizationProblem, model_parser: ModelParser, params_as_vars: bool):
    X = op.optvars.variables_by_names(model_parser.variables.states.names)
    if model_parser.variables.states.n_vars > 0:
        X = X.reshape((-1, model_parser.variables.states.n_vars)).T

    U = op.optvars.variables_by_names(model_parser.variables.inputs.names)
    if model_parser.variables.inputs.n_vars > 0:
        U = U.reshape((-1, model_parser.variables.inputs.n_vars)).T

    if params_as_vars:
        Params = op.optvars.variables_by_names(model_parser.variables.parameters.names).reshape((-1,model_parser.variables.parameters.n_vars)).T
    else:
        Params = op.problem_parameters.variables_flat()

    return [X, U, Params]


def mk2(ode_variable, ode_equation, op, model_parser: ModelParser, dt, params_as_vars = False):
    [X, U, Params] = prepare_variables(op, model_parser, params_as_vars)

    der_variable_name = ode_variable.replace('der(', '').replace(")", "")
    odes_x = op.optvars.variables_by_names(der_variable_name)
    dynamic_func = parse_to_casadi_function(model_parser.variables, ode_equation)

    odes_x0 = odes_x[:-1]
    odes_x1 = odes_x[1:]

    X0 = X[:,:-1]
    U0 = U
    K1 = dynamic_func(X0, U0, Params)

    dynamic_const = odes_x0 + dt * K1.T - odes_x1
    return dynamic_const


def mk3(ode_variable, ode_equation, op, model_parser: ModelParser, dt, params_as_vars = False):
    [X, U, Params] = prepare_variables(op, model_parser, params_as_vars)

    der_variable_name = ode_variable.replace('der(', '').replace(")", "")
    odes_x = op.optvars.variables_by_names(der_variable_name)
    dynamic_func = parse_to_casadi_function(model_parser.variables, ode_equation)

    odes_x0 = odes_x[:-1]
    odes_x1 = odes_x[1:]

    X0 = X[:,:-1]
    U0 = U
    K1 = dynamic_func(X0, U0, Params)
    ode_x_row = [k for k in range(len(op.optvars.idxs.keys())) if der_variable_name == list(op.optvars.idxs.keys())[k]][0]
    X1 = X[:,1:]
    X1[ode_x_row, :] += dt * K1
    K2 = dynamic_func(X1, U0, Params)
    dynamic_const = odes_x0 + dt * ( K1 + K2).T / 2. - odes_x1
    return dynamic_const
