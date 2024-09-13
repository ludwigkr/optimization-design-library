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

    nlopt_set_min_objective(optimizer, objective_fn, NULL);
    nlopt_add_inequality_mconstraint(optimizer, N_XOPTS, constraint_fn, static_cast<void *>(&prob_data), &tolerance);

    nlopt_set_xtol_rel(optimizer, tolerance);


    initial_guess_fn(x, N_XOPTS, x, static_cast<void *>(&prob_data));
    double minf;
    auto status = nlopt_optimize(optimizer, x, &minf);

    optimized_variable_fn(&xopt, N_XOPTS, x);

    return status;
}
