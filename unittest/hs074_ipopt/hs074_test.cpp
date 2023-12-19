#include "hs074_interface.h"
#include "../../cpp/test_case_importer.h"
#include <iostream>
#include <CppUTest/TestHarness.h> //include at last!

TEST_GROUP(HS074) {
};

TEST(HS074, functiontest) {
    TestCaseImporter case_importer = TestCaseImporter("../../testcase_data/test_build_ipopt/test_hs074.json");
    case_importer.load_json();
    uint N = case_importer.amount_cases(); 

    Hs074_Interface optimizer = Hs074_Interface();
    scenario_parameter scenario;
    problem_parameter prob_param;
    optimized_variable xref;

    case_importer.test_cast(0, &scenario, &prob_param, &xref);

    optimizer.scenario = scenario;
    optimizer.prob_param = prob_param;

    optimizer.solve();
    optimized_variable result = optimizer.xopt;

    float error = (result - xref).norm();
    CHECK(error<1e-3);
};

