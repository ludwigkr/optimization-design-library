import re
from model_variables import ModelVariables
from model_equations import ModelEquations

class ModelParser:
    def __init__(self, model_text):
        model_text = re.sub(r'(?<=[A-Za-z0-9])\.(?=[A-Za-z])', '_' , model_text)
        self.model_lines = model_text.split("\n")
        self.model_name = self.model_lines[0].replace("class ", "").replace("model ", "")
        self.variables = ModelVariables(self.model_lines)
        self.equations = ModelEquations(self.model_lines)


if __name__ == "__main__":

    file_path = "../../appartment-heat-optimization/oscillator.txt"
    with open(file_path, "r") as f:
        model_text = f.read()

    parser = ModelParser(model_text)
    print(f"Parameters({len(parser.variables.parameters)}):")
    for p in parser.variables.parameters:
        print(p)
    print()

    print(f"Variables({len(parser.variables.states)}):")
    for v in parser.variables.states:
        print(v)
    print()

    print(f"ODEs ({len(parser.equations.odes)}):")
    for e in parser.equations.odes:
        print(e)
    print()

    print(f"Equaions ({len(parser.equations.constraints)}):")
    for e in parser.equations.constraints:
        print(e)
