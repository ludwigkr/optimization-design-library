import casadi
from model_variables import ModelVariables

def create_op_mapping(model_variables: ModelVariables):
    mapping = {'sin': casadi.sin, 'cos': casadi.cos}

    xopt = model_variables.states.unpacked()
    if type(xopt) == casadi.SX:
        for x in range(xopt.size1()):
            mapping[str(xopt[x])] = xopt[x]

    uopt = model_variables.inputs.unpacked()
    if type(uopt) == casadi.SX:
        for u in range(uopt.size1()):
            mapping[str(uopt[u])] = uopt[u]

    prob_params = model_variables.parameters.unpacked()
    if type(prob_params) == casadi.SX:
        for p in range(prob_params.size1()):
            mapping[str(prob_params[p])] = prob_params[p]
    return mapping

def parse_to_casadi_function(model_variables: ModelVariables, formula: str):

    mapping = create_op_mapping(model_variables)
    if formula[-1] == ";":
        formula = formula[:-1]

    expression = eval(formula, mapping)
    func = casadi.Function("c1", [model_variables.states.unpacked(), model_variables.inputs.unpacked(), model_variables.parameters.unpacked()], [expression])
    return func
