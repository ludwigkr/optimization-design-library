import os
import json
import numpy as np
from variables import Variables
import casadi
from optimizationproblem import OptimizationProblem

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
