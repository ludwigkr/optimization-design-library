
#include "min_nlp_interface.h"
#include <chrono>
#include <iostream>

#include <CppUTest/TestHarness.h> //include at last!

TEST_GROUP(MinNLP) {
    MinNLPInterface opti;
};

TEST(MinNLP, test_case) {
    opti.init();
    Eigen::VectorXd sp(2);
    sp[0] = 10;
    sp[1] = 10;
    auto opti_res = opti.find_optimal_solution(sp);
    Eigen::VectorXd Xopt_check(2);
    Xopt_check << 2.5, 4.5;
    CHECK((opti_res-Xopt_check).norm()<1e-6);
}
