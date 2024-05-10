import casadi

def parse_om_function_to_casadi(model_vars, formula_str):
    def create_op_mapping(model_vars):
        mapping = {'sin': casadi.sin, 'cos': casadi.cos}

        xopt = model_vars.X.unpacked()
        if type(xopt) == casadi.SX:
            for x in range(xopt.size1()):
                mapping[str(xopt[x])] = xopt[x]

        uopt = model_vars.U.unpacked()
        if type(uopt) == casadi.SX:
            for u in range(uopt.size1()):
                mapping[str(uopt[u])] = uopt[u]

        prob_params = model_vars.params.unpacked()
        if type(prob_params) == casadi.SX:
            for p in range(prob_params.size1()):
                mapping[str(prob_params[p])] = prob_params[p]
        return mapping

    mapping = create_op_mapping(model_vars)
    if formula_str[-1] == ";":
        formula_str = formula_str[:-1]

    expression = eval(formula_str, mapping)
    func = casadi.Function("c1", [model_vars.X.unpacked(), model_vars.U.unpacked(), model_vars.params.unpacked()], [expression])
    return func
