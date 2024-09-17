#pragma once
#include <math.h>
#include "problem_formulation.hpp"


class Problem {
public:
    problem_data prob_data;
    scenario_parameter *scenario;
    problem_parameter *prob_param;
    optimized_variable xopt;
    optimizer_info opt_info;
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

    double minf;
    double lbx[N_XOPTS];
    double ubx[N_XOPTS];
    double x[N_XOPTS];
    nlopt_opt optimizer;
    const double tolerance = 1e-8;

    void eval_optimizer_result(nlopt_result status);
};
