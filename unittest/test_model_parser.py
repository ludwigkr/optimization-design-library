import unittest
import sys

sys.path.append("../openmodelica_parser")
from model_parser import ModelParser


class TestFlatOMModelImporter(unittest.TestCase):
    def setUp(self):
        pass

    def test_parse_oscillator(self):
        oscillator_path = "./testdata/om_flat_oscillator.txt"

        with open(oscillator_path, "r") as f:
            model_text = f.read()

        parser = ModelParser(model_text)
        self.assertTrue(len(parser.equations.constraints) == 26)
        self.assertTrue(len(parser.equations.odes) == 3)
        self.assertTrue(len(parser.variables.states) == 29)
        self.assertTrue(len(parser.variables.parameters) == 12)
        pass

    def test_parse_PT1(self):
        oscillator_path = "./testdata/PT1.txt"

        with open(oscillator_path, "r") as f:
            model_text = f.read()

        parser = ModelParser(model_text)
        self.assertTrue(len(parser.equations.constraints) == 1)
        self.assertTrue(len(parser.equations.odes) == 1)
        self.assertTrue(len(parser.variables.states) == 3)
        self.assertTrue(len(parser.variables.parameters) == 3)

if __name__ == "__main__":
    unittest.main()
