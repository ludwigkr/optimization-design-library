import re

def read_model(model_path):
    with open(model_path, "r") as f:
        model_text = f.read()
    return model_text