import os
from pathlib import Path
local_folder_path = Path(os.path.dirname(os.path.abspath(__file__)))

import sys
sys.path.append(f'{local_folder_path}/../')
from optimizationproblem import OptimizationProblem

def initialize_cmake_project(op: OptimizationProblem, target_folder: str):
    target_file = f"{target_folder}/CMakeLists.txt"
    if not os.path.exists(target_file):
        with open(f'{local_folder_path}/CMakeLists.txt', 'r') as f:
            cmake = f.read()

        cmake = cmake.replace('<problem_name>', op.name)

        with open(target_file, "w") as f:
            f.write(cmake)

if __name__ == "__main__":
    initialize_cmake_project(OptimizationProblem(), '/tmp')


    