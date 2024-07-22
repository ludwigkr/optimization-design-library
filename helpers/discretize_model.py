import casadi
from model_parser import ModelParser
from parse_to_casadi_function import parse_to_casadi_function

def mk2(ode_variable, ode_equation, op, model_parser: ModelParser, dt):
        X = op.optvars.variables_by_names(model_parser.variables.states.names).reshape((-1,model_parser.variables.states.n_vars)).T
        U = op.optvars.variables_by_names(model_parser.variables.inputs.names).reshape((-1,model_parser.variables.inputs.n_vars)).T
        Params = op.problem_parameters.variables_flat()

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
        

def mk3(ode_variable, ode_equation, op, model_parser: ModelParser, dt):
        X = op.optvars.variables_by_names(model_parser.variables.states).reshape((-1,len(model_parser.variables.states))).T
        U = op.optvars.variables_by_names(model_parser.variables.inputs).reshape((-1,len(model_parser.variables.inputs))).T
        Params = op.problem_parameters.variables_flat()

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

