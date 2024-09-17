#include <iostream>
#include "nlopt_example_interface.hpp"

auto main(int argc, char *argv[]) -> int {
    NloptExampleProblem example_problem;
    example_problem.init(NLOPT_LD_MMA);
    example_problem.scenario.init_guess << 1.234, 5.678;
    example_problem.prob_param.aparam << 2, -1;
    example_problem.prob_param.bparam << 0, 1;
    example_problem.solve();

    std::cout << example_problem.xopt << std::endl;
    std::cout << example_problem.opt_info << std::endl;

    return 0;
}
