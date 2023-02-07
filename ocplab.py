#!/usr/bin/env python3
import casadi

import ocp

class OCPLab():
    def __init__(self):
        self.op = ocp.OptimalProblem()
