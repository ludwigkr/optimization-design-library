#!/usr/bin/env python3

def class_name(name: str, quadratic_optimier=False) -> str:
    name = name.replace("_", " ")
    name = name.title()
    name = name.replace(" ", "")
    if quadratic_optimier:
        name = name + "QuadraticOptimizer"
    return name

