#include <math.h>
#include <iostream>
#include "nlopt_problem_interface.hpp"
#include "problem_formulation.hpp"


void Problem::init(nlopt_algorithm algorythm) {
    optimizer = nlopt_create(algorythm, N_XOPTS);
}

int Problem::solve() {

    lower_bound_fn(lbx, N_XOPTS, x, static_cast<void *>(&prob_data));
    nlopt_set_lower_bounds(optimizer, lbx);

    upper_bound_fn(ubx, N_XOPTS, x, static_cast<void *>(&prob_data));
    nlopt_set_upper_bounds(optimizer, ubx);

    nlopt_set_min_objective(optimizer, objective_fn, static_cast<void *>(&prob_data));
    nlopt_add_inequality_mconstraint(optimizer, N_XOPTS, constraint_fn, static_cast<void *>(&prob_data), &tolerance);

    nlopt_set_xtol_rel(optimizer, tolerance);
    initial_guess_fn(x, N_XOPTS, x, static_cast<void *>(&prob_data));

    nlopt_result status = nlopt_optimize(optimizer, x, &minf);

    optimized_variable_fn(&xopt, N_XOPTS, x);
    eval_optimizer_result(status);

    return status;
}

void Problem::eval_optimizer_result(nlopt_result status) {
    opt_info.costs = minf;
    opt_info.status = status;
    for (uint i = 0; i < N_XOPTS; i++) {
        if (abs(x[i] - lbx[i]) < 1e-3) {
            opt_info.active_box_limits[i] = true;
        } else if (abs(x[i] - ubx[i]) < 1e-3) {
            opt_info.active_box_limits[i] = true;
        } else {
            opt_info.active_box_limits[i] = false;
        }

        if ((lbx[i] - x[i] > 1e-4) || (x[i] - ubx[i] > 1e-4)) {
            opt_info.violated_box_limits[i] = true;
        } else {
            opt_info.violated_box_limits[i] = false;
        }

    }

    double constraint_values[N_CONSTRAINTS] = {0};
    constraint_fn(N_CONSTRAINTS, constraint_values, N_XOPTS, x, NULL, static_cast<void *>(&prob_data));
    for (uint i = 0; i < N_CONSTRAINTS; i++) {
        if (abs(constraint_values[i]) < 1e-3) {
            opt_info.active_constraints[i] = true;
        } else {
            opt_info.active_constraints[i] = false;
        }

        if (constraint_values[i] > 1e-4) {
            opt_info.violated_constraints[i] = true;
        } else {
            opt_info.violated_constraints[i] = false;
        }
    }

}
