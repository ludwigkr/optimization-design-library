#pragma once
#include <math.h>
#include <nlopt.h>
#include "problem_formulation.hpp"

#define N_XOPTS nxopts

class Problem {
public:
    problem_data prob_data;
    scenario_parameter *scenario;
    problem_parameter *prob_param;
    optimized_variable xopt;
    int solve();
    void init(nlopt_algorithm algorythm);
    Problem() {
        scenario = &(prob_data.scenario);
        prob_param = &(prob_data.prob_param);
    }
    ~Problem() {
        nlopt_destroy(optimizer);
    }

private:

    double lbx[N_XOPTS];
    double ubx[N_XOPTS];
    double x[N_XOPTS];
    nlopt_opt optimizer;
    double objective(unsigned n, const double *x, double *grad, void *my_func_data);
    const double tolerance = 1e-8;

};
