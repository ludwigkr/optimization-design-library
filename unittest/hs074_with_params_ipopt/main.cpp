#include "hs074_interface.h"
#include "../../cpp/test_case_importer.h"
#include <iostream>

int main(int, char **) {
    TestCaseImporter case_importer = TestCaseImporter("../../testcase_data/test_build_ipopt/test_hs074_with_params.json");
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
    std::cout << "xopt: " << result << std::endl;
    std::cout << "xref: " << std::endl << xref << std::endl;
    std::cout << "error: " << std::endl << error << std::endl;

    return 0;
}