
class ModelEquations:
    """Parses model text to list of equation strings."""

    def __init__(self, model_lines=None) -> None:
        self.odes = []
        self.constraints = []

        if model_lines is not None:
            equation_lines = self.find_equation_lines(model_lines)
            for eq_line in equation_lines:
                parsed_eq_line = self.parse_equation_line(eq_line)
                eq_type = self.determine_type(eq_line)
                self.assign_based_on_type(parsed_eq_line, eq_type)

    def find_equation_lines(self, model_lines: [str]) -> [str]:
        start_idx = model_lines.index("equation")
        end_idx = [line_idx for line_idx, line in enumerate(model_lines) if line[:3] == 'end'][0]

        return model_lines[start_idx+1:end_idx]


    def parse_equation_line(self, eq_line):
        eq_line = eq_line.replace("  ", "").replace(";","")
        return eq_line


    def determine_type(self, eq_line):
        if 'der(' in eq_line:
            return 'ode'
        else:
            return 'constraint'

    def assign_based_on_type(self, eq_line, eq_type):
        if eq_type == 'ode':
            self.odes.append(eq_line)
        else:
            self.constraints.append(eq_line)
