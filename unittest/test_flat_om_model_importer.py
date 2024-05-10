import unittest
import sys

sys.path.append("../openmodelica_parser")
from flat_om_model_importer import ModelParser


class TestFlatOMModelImporter(unittest.TestCase):
    def setUp(self):
        pass

    def test_parse_oscillator(self):
        oscillator_path = "./testdata/om_flat_oscillator.txt"

        with open(oscillator_path, "r") as f:
            model_text = f.read()

        parser = ModelParser(model_text)
        self.assertTrue(len(parser.equations) == 26)
        self.assertTrue(len(parser.variables) == 27)
        self.assertTrue(len(parser.parameters) == 8)
        pass


if __name__ == "__main__":
    unittest.main()
