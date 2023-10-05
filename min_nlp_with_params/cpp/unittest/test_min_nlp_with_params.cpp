#include "../min_nlp_with_params_problem_ipopt.h"
#include "../min_nlp_with_params_interface.h"
#include "../../../cpp/test_case_importer.h"
#include <iostream>

#include <CppUTest/TestHarness.h> //include at last!

using json = nlohmann::json;

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

TEST(MinNlpWithParams, pythonTests) {
    TestCaseImporter case_importer = TestCaseImporter("./../../../tests_min_nlp_with_params.json");
    case_importer.load_json();
    uint N = case_importer.amount_cases();

    scenario_parameter scenario;
    problem_parameter prob_param;
    optimized_variable xref;
    MinNlpWithParams_Interface minnlpwithparams;
    for (uint i=0; i<N; i++) {
        case_importer.test_cast(0, &scenario, &prob_param, &xref);
        minnlpwithparams.scenario = scenario;
        minnlpwithparams.prob_param = prob_param;
        
        minnlpwithparams.solve();
        optimized_variable result = minnlpwithparams.xopt;
        CHECK( (result - xref).norm() < 1e-5);
    }
}
