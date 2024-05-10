import re

class ModelParser:
    def __init__(self, model_text):
        self.model_lines = model_text.split("\n")
        self.model_name = self.model_lines[0].replace("class ", "")

        self.parameters = self.parse_parameters()
        self.variables = self.parse_variables()
        [self.odes, self.equations] = self.parse_equations()

    def parse_parameters(self) -> [str]:
        def find_parameter_lines(model_lines) -> [str]:
            parameter_lines = []
            for line in model_lines:
                if line[:11] == "  parameter":
                    parameter_lines.append(line)
            return parameter_lines

        def parse_parameter_lines(parameter_lines) -> [str]:
            params = []
            for p in parameter_lines:
                params.append(p[17:].split("(")[0])

            return params

        parameter_lines = find_parameter_lines(self.model_lines)
        return parse_parameter_lines(parameter_lines)

    def parse_variables(self) -> [str]:
        def find_variable_lines(model_lines) -> [str]:
            variable_lines = []
            for line in model_lines:
                if line[:7] == "  Real ":
                    variable_lines.append(line)
            return variable_lines

        def parse_variable_lines(variable_lines) -> [str]:
            vars = []
            for v in variable_lines:
                if "(" in v:
                    vars.append(v[7:].split("(")[0])

            return vars

        variables_lines = find_variable_lines(self.model_lines)
        return parse_variable_lines(variables_lines)

    def parse_equations(self):
        start_idx = self.model_lines.index("equation")
        end_idx = self.model_lines.index(f"end {self.model_name};")
        equation_lines = self.model_lines[start_idx+1:end_idx]

        equations = []
        for e in equation_lines:
            equations.append(e.replace("  ", "").replace(";",""))

        odes = []
        for e in reversed(equations):
            if 'der(' in e:
                odes.append(e)
                equations.remove(e)

        return [odes, equations]


if __name__ == "__main__":

    file_path = "../../appartment-heat-optimization/oscillator.txt"
    with open(file_path, "r") as f:
        model_text = f.read()

    parser = ModelParser(model_text)
    print(f"Parameters({len(parser.parameters)}):")
    for p in parser.parameters:
        print(p)
    print()

    print(f"Variables({len(parser.variables)}):")
    for v in parser.variables:
        print(v)
    print()

    print(f"ODEs ({len(parser.odes)}):")
    for e in parser.odes:
        print(e)
    print()

    print(f"Equaions ({len(parser.equations)}):")
    for e in parser.equations:
        print(e)
