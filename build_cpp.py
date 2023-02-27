#!/usr/bin/env python3
import os
import sys
local_folder_path = os.path.dirname(__file__)
sys.path.append(local_folder_path + "/qpoases_builder")
from build_qpoases import QpoasesBuilder
from optimizationproblem import OptimizationProblem
from qpelements import QuadraticOptimizerElements

class CppBuilder:
    def __init__(self) -> None:
        self.build_qpoases = True
        pass

    def build(self, op: OptimizationProblem, path=None) -> None:
        self.quadratic_elements = QuadraticOptimizerElements(op)
        if self.build_qpoases:
            qpoases_builder = QpoasesBuilder()
            qpoases_builder.build(op, self.quadratic_elements, path)


        pass
