#include <iostream>
#include "test_case_importer.h"

void TestCaseImporter::load_json() {
    std::ifstream f(filepath);
    data = json::parse(f);
}

std::tuple<std::map<std::string, size_t>, std::map<std::string, size_t>, std::map<std::string, size_t>> mappers();

void TestCaseImporter::test_cast(int n, scenario_parameter* scenario, problem_parameter* prob_param, optimized_variable* xopt){

    std::map<std::string, size_t> map_scenario;
    std::map<std::string, size_t> map_prob_param;
    std::map<std::string, size_t> map_xopt;
    std::tie(map_scenario, map_prob_param, map_xopt) = mappers();


   for (const auto& item : data["cases"][n]["scenario"].items()) {
        size_t offset = map_scenario[item.key()];
        if(item.value().size()>1) {
            Eigen::VectorXd* element_pnt = static_cast<Eigen::VectorXd*>(static_cast<void*>(scenario) + offset);
            *element_pnt = parse_vector(n, "scenario", item.key());
        } else {
            float* element_pnt = static_cast<float*>(static_cast<void*>(scenario) + offset);
            *element_pnt = parse_number(n, "scenario", item.key());
        }
    }

   for (const auto& item : data["cases"][n]["prob_param"].items()) {
        size_t offset = map_prob_param[item.key()];
        if(item.value().size()>1) {
            Eigen::VectorXd* element_pnt = static_cast<Eigen::VectorXd*>(static_cast<void*>(prob_param) + offset);
            *element_pnt = parse_vector(n, "prob_param", item.key());
        } else {
            float* element_pnt = static_cast<float*>(static_cast<void*>(prob_param) + offset);
            *element_pnt = parse_number(n, "prob_param", item.key());
        }
    }

   for (const auto& item : data["cases"][n]["xopt"].items()) {
        size_t offset = map_xopt[item.key()];
        if(item.value().size()) {
            Eigen::VectorXd* element_pnt = static_cast<Eigen::VectorXd*>(static_cast<void*>(xopt) + offset);
            *element_pnt = parse_vector(n, "xopt", item.key());
        } else {
            float* element_pnt = static_cast<float*>(static_cast<void*>(xopt) + offset);
            *element_pnt = parse_number(n, "xopt", item.key());
        }
    }
}

Eigen::VectorXd TestCaseImporter::parse_vector(int n, std::string struct_key, std::string key) {

    std::vector<float> s = data["cases"][n][struct_key][key];
    Eigen::VectorXd ret = Eigen::VectorXd(s.size());
    for(uint i=0; i<s.size(); i++) {
        ret[i] = s[i];
    }
    return ret;
}

float TestCaseImporter::parse_number(int n, std::string struct_key, std::string key) {
    float ret = data["cases"][n][struct_key][key];
    return ret;
}