
#include "min_nlp_interface.h"
#include <chrono>
#include <iostream>

#include <CppUTest/TestHarness.h> //include at last!

TEST_GROUP(MinNLP) {
    MinNLPInterface opti;
};

TEST(MinNLP, functiontest_casadi) {

    opti.init();
    // opti.init_casadi("../../ocp_design/casadi/min_nlp/min_nlp_optimizer.so");
    // opti.use_trustregionmethod = true;
    Eigen::VectorXd sp(2);
    sp[0] = 0;
    sp[1] = 0;
    auto opti_res = opti.find_optimal_solution(sp);
    // std::cout << "Xopt:" << opti_res.transpose() << std::endl;

    CHECK(opti_res.norm()<1e-6);
}
