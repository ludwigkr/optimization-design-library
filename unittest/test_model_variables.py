
import unittest
import sys

sys.path.append("../openmodelica_parser")
from model_variables import ModelVariables

class TestModelVariables(unittest.TestCase):
    def setUp(self):
        pass

    def test_basic_lines(self):
        parser = ModelVariables()
        with self.subTest("default line with brackets and initialization"):
            test_line = 'parameter Real mass2.m(quantity = "Mass", unit = "kg", min = 0.0, start = 1.0) = 1.0 "Mass of the sliding mass";'
            ret = parser.extract_variable_name(test_line)
            self.assertTrue(ret == 'mass2_m')

        with self.subTest("with final keyword"):
            test_line = 'final parameter enumeration(never, avoid, default, prefer, always) mass2.stateSelect = StateSelect.default "Priority to use s and v as states";'
            ret = parser.extract_variable_name(test_line)
            self.assertTrue(ret == 'enumeration')

        with self.subTest("simple state"):
            test_line = ' Real mass2.flange_a.f(quantity = "Force", unit = "N") "Cut force directed into flange"; '
            ret = parser.extract_variable_name(test_line)
            self.assertTrue(ret == 'mass2_flange_a_f')

        with self.subTest("extra stuff without brackets"):
            test_line = 'Real force_input.y "Connector of Real output signal";'
            ret = parser.extract_variable_name(test_line)
            self.assertTrue(ret == 'force_input_y')
        pass

    def test_parse_oscillator(self):
        oscillator_path = "./testdata/om_flat_oscillator.txt"

        with open(oscillator_path, "r") as f:
            model_text = f.read()

        parser = ModelVariables(model_text.split("\n"))
        self.assertTrue(len(parser.inputs) == 0)
        self.assertTrue(len(parser.outputs) == 0)
        self.assertTrue(len(parser.states) == 29)
        self.assertTrue(len(parser.parameters) == 12)
        pass


    def test_parse_PT1(self):
        oscillator_path = "./testdata/PT1.txt"

        with open(oscillator_path, "r") as f:
            model_text = f.read()

        parser = ModelVariables(model_text.split("\n"))
        self.assertTrue(len(parser.inputs) == 0)
        self.assertTrue(len(parser.outputs) == 0)
        self.assertTrue(len(parser.states) == 3)
        self.assertTrue(len(parser.parameters) == 3)

        with self.subTest("test_inputs_are"):
            parser.inputs_are(['u'])
            self.assertTrue(len(parser.inputs) == 1)
            self.assertTrue(len(parser.outputs) == 0)
            self.assertTrue(len(parser.states) == 2)
            self.assertTrue(len(parser.parameters) == 3)


if __name__ == "__main__":
    unittest.main()
