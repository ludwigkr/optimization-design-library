"""."""

def load_optimizer_settings(optimizer='sqpmethod', quadratic_optimizer="qpoases"):
    """."""
    optimizer_settings = {"optimizer": optimizer}
    if optimizer == 'sqpmethod':
        if quadratic_optimizer == "qpoases":
            optimizer_settings["options"] = {"qpsol":"qpoases",
                    "verbose": False,
                    "print_time": False,
                    "print_status": True,
                    "print_header": True,
                    "print_iteration": False,
                    "convexify_strategy": "regularize", #NONE|regularize|eigen-reflect|eigen-clip.
                    "hessian_approximation": "exact", #limited-memory|exact
                    "max_iter": 1000,
                    "qpsol_options": {
                                    "printLevel":"none",
                                    "error_on_fail": False
                                    }
                    }
        elif quadratic_optimizer == "osqp":
            optimizer_settings["options"] = {
                "qpsol": "osqp",
                'expand': False,
                "error_on_fail": False,
                "qpsol_options": {
                    #"max_iter": 1000,
                    # "adaptive_rho": True,
                    "verbose": False,
                    "error_on_fail": False
                }
            }
    else:
        optimizer_settings["optimizer"] = 'ipopt'
        optimizer_settings["options"] = {'print_time': True,
                        'ipopt': {'max_iter': 500,
                        'bound_mult_init_method': 'mu-based',
                        'nlp_scaling_method': 'gradient-based'
                        }}

    return optimizer_settings

## QRQP doesn't seem to work with sqp
# opts = {"qpsol":"qrqp",
        # "qpsol_options": {"print_problem":False,
                          # "error_on_fail": True},
        # "convexify_strategy":"regularize",
        # "convexify_margin":1e-4}

# --------------QPOASES---------------------
# opts = {
# }

# solver = casadi.qpsol('solver', 'qpoases', {'x': Xopt_flat, 'p': Params_flat,
                                         # 'f': objective, 'g': constraints}, opts)

# ------------- OSQP ---------------------
# solvername = "osqp"
# opts = {
    # 'expand': False,
    # "error_on_fail": True,
    # "osqp": {
        # #"max_iter": 1000,
        # "adaptive_rho": 0,
        # "verbose": False
    # }
# }
# ------------------------------------------
