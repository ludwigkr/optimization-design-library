#include "min_nlp_interface.h"

void MinNLPInterface::init() {
    qpsolver.init();
    sqpsolver.init(&qpsolver);
}

Eigen::VectorXd MinNLPInterface::find_optimal_solution(Eigen::VectorXd init_guess_params) {
    scenario_parameter scenario(init_guess_params);
    problem_parameter prob_param;
    quadratic_problem_values quad_prob_values;

    quad_prob_values.X0 = qpsolver.initial_guess(&prob_param, &scenario);
    quad_prob_values.lbx = qpsolver.lbx(&prob_param, &scenario);
    quad_prob_values.ubx = qpsolver.ubx(&prob_param, &scenario);
    quad_prob_values.lbg = qpsolver.lbg(&prob_param, &scenario);
    quad_prob_values.ubg = qpsolver.ubg(&prob_param, &scenario);

    Eigen::VectorXd Xopt = sqpsolver.solve_line_search(&quad_prob_values);

    return Xopt;

}
