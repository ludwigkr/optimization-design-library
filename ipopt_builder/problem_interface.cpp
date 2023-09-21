#include "problem_formulation_interface.h"
#include <iostream>

Problem_Interface::Problem_Interface() {
    mynlp = new ProblemFormulation(&scenario, &prob_param, &xopt);
    app = IpoptApplicationFactory();
    app->Options()->SetStringValue("sb", "yes");
    app->Options()->SetIntegerValue("print_level", 0);
    status;
}

int Problem_Interface::solve() {
    status = app->Initialize();
    if (status != Solve_Succeeded) {
        std::cout << std::endl << std::endl << "*** Error during initialization!" << std::endl;
        return (int) status;
    }

    status = app->OptimizeTNLP(mynlp);

    // if (status == Solve_Succeeded) {
    //     Index iter_count = app->Statistics()->IterationCount();
    //     // std::cout << std::endl << std::endl << "*** The problem solved in " << iter_count << " iterations!" << std::endl;

    //     Number final_obj = app->Statistics()->FinalObjective();
    //     std::cout << std::endl << std::endl << "*** The final value of the objective function is " << final_obj << '.' << std::endl;
    // }

    return (int) status;
}
