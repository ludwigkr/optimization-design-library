#!/usr/bin/env python3
import unittest
import inspect
import re
import os

class ParserTestCase(unittest.TestCase):
    # def __init__(self):
    #     self.mode = "unittest" # 'unittest'|'set_reference'

    def identify_caller(self):
        context = str(inspect.stack()[2][0])
        tester_name = context.split("'")[1].split("/")[-1].split(".")[0]
        case_name = context.split(" ")[-1][:-1]
        return tester_name, case_name

    def folder(self, tester_name) -> str:
        return f"testcase_data/{tester_name}"

    def json_file_path(self):
        tester_name, case_name = self.identify_caller()
        folder = self.folder(tester_name)
        return f"{folder}/{case_name}.json"

    def save_reference(self, reference):
        tester_name, case_name = self.identify_caller()
        folder = self.folder(tester_name)
        if not os.path.exists(folder):
            os.makedirs(folder)

        with open(f"{folder}/{case_name}.txt", "w") as f:
            f.write(reference)

    def load_reference(self):
        tester_name, case_name = self.identify_caller()
        _file = self.folder(tester_name) + f"/{case_name}.txt"

        if os.path.exists(f"{_file}"):
            with open(f"{_file}", "r") as f:
                return f.read()
        else:
            print(f"Unittest data for {tester_name} - {case_name} doesn't exis yet.")
            return False
