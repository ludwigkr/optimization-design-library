#include "../min_nlp_with_params_interface.h"
#include <iostream>


int main(int ac, char **av) {
    Eigen::VectorXd SP = Eigen::VectorXd(2);
    SP << 10, 10;
    float p = 2;
    scenario_parameter scenario = scenario_parameter(SP);
    problem_parameter prob_param = problem_parameter(p);

    MinNlpWithParams_Interface minnlpwithparams;
    minnlpwithparams.prob_param = prob_param;
    minnlpwithparams.scenario = scenario;
    int status = minnlpwithparams.solve();
    optimized_variable result = minnlpwithparams.xopt;
    std::cout << "xopt: " << result << std::endl;
}
