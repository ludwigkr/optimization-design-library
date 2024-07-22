import sys
import re
sys.path.append("..")
from variables import Variables

class ModelVariables:
    """Parses model text to list of variable names."""

    def __init__(self, model_lines=None) -> None:
        self.parameters = []
        self.inputs = []
        self.states = []
        self.outputs = []
        self.disturbances = []

        if model_lines is not None:
            variable_lines = self.find_variable_lines(model_lines)
            for variable_line in variable_lines:
                var = self.extract_variable_name(variable_line)
                self.assign_to_variables(var, variable_line)
        pass

    def extract_variable_name(self, variable_line:str) -> str:

        if "(" in variable_line:
            variable_line = variable_line.split("(")[0]

        if variable_line[-1] == ';':
            variable_line = variable_line[:-1]

        words = variable_line.split(" ")
        try:
            equal_idx = words.index("=")
            if equal_idx:
                words = words[:equal_idx]
        except:
            pass

        try:
            quote_idx = [word_idx for word_idx, word in enumerate(words) if '"' in word][0]
            if quote_idx:
                words = words[:quote_idx]
        except:
            pass

        var = words[-1].replace(".", "_")

        return var

    def assign_to_variables(self, var, variable_line):
        var_type = self.determin_variable_type(variable_line)

        if var_type == 'param':
            self.parameters.append(var)
        elif var_type == 'input':
            self.inputs.append(var)
        elif var_type == 'output':
            self.outputs.append(var)
        elif var_type == 'state':
            self.states.append(var)

    def determin_variable_type(self, variable_line):
        if 'parameter' in variable_line:
            return 'param'
        elif "Modelica_Blocks_Interfaces_RealInput" in variable_line:
            return 'input'
        elif "Modelica_Blocks_Interfaces_RealOutput" in variable_line:
            return 'output'
        else:
            return 'state'


    def parse_variables(self, model_lines) -> [str]:
        def find_variable_lines(model_lines) -> [str]:
            variable_lines = []
            for line in model_lines:
                if line[:7] == "  Real ":
                    variable_lines.append(line)
                if line[:38] == "  Modelica_Blocks_Interfaces_RealInput":
                    variable_lines.append(line)
                if line[:39] == "  Modelica_Blocks_Interfaces_RealOutput":
                    variable_lines.append(line)
            return variable_lines


    def find_variable_lines(self, model_lines: [str]) -> [str]:
        start_idx = 1
        end_idx = model_lines.index('equation')
        return model_lines[start_idx:end_idx]

    def inputs_are(self, inputs_list: [str]) -> None:
        for input in inputs_list:
            input_name = input.replace('.', '_')
            if input_name in reversed(self.states):
                self.states.remove(input_name)
                inputs_list.remove(input)
                self.inputs.append(input_name)

        if len(inputs_list) > 0:
            raise(Warning(f"Not all inputs found in states. The following are not found: {inputs_list}"))

    def convert_variables_to_symbolics(self):

        param = Variables()
        for p in self.parameters:
            param.register(p)
        self.parameters = param

        inputs = Variables()
        for u in self.inputs:
            inputs.register(u)
        self.inputs = inputs

        states = Variables()
        for x in self.states:
            states.register(x)
        self.states = states

        outputs = Variables()
        for o in self.outputs:
            outputs.register(o)
        self.outputs = outputs

        disturbances = Variables()
        for d in self.disturbances:
            disturbances.register(d)
        self.disturbances = disturbances
