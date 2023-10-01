#include "../min_nlp_with_params_interface.h"
#include <iostream>
#include <CppUTest/TestHarness.h> //include at last!

TEST_GROUP(MinNlpWithParams) {
    void setup() {
    }
    void teardown() {}
};


TEST(MinNlpWithParams, simpleTest) {
    Eigen::VectorXd SP = Eigen::VectorXd(2);
    SP << 10, 10;
    float p = 2;
    scenario_parameter scenario = scenario_parameter(SP);
    problem_parameter prob_param = problem_parameter(p);

    MinNlpWithParams_Interface minnlpwithparams;
    minnlpwithparams.scenario = scenario;
    minnlpwithparams.prob_param = prob_param;
    minnlpwithparams.solve();
    optimized_variable result = minnlpwithparams.xopt;

    Eigen::VectorXd Xref{{1.02273, 4.04545}};
    CHECK((Xref - result.X).norm() < 1e5);
}
