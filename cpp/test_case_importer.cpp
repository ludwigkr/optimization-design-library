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

    parse_struct("scenario", static_cast<void*>(scenario), map_scenario, n);
    parse_struct("prob_param", static_cast<void*>(prob_param), map_prob_param, n);
    parse_struct("xopt", static_cast<void*>(xopt), map_xopt, n);
}

#pragma GCC diagnostic push
#pragma GCC diagnostic ignored "-Wpointer-arith"
void TestCaseImporter::parse_struct(std::string struct_name, void* structure, std::map<std::string, size_t> mapper, int case_nr) {
   for (const auto& item : data["cases"][case_nr][struct_name].items()) {
        size_t offset = mapper[item.key()];
        if(item.value().is_array()) {
            if(item.value()[0].is_array()) {
                Eigen::MatrixXd* element_pnt = static_cast<Eigen::MatrixXd*>(static_cast<void*>(structure) + offset);
                *element_pnt = parse_matrix(case_nr, struct_name, item.key());
            } else {
                Eigen::VectorXd* element_pnt = static_cast<Eigen::VectorXd*>(static_cast<void*>(structure) + offset);
                *element_pnt = parse_vector(case_nr, struct_name, item.key());
            }
        } else {
            float* element_pnt = static_cast<float*>(static_cast<void*>(structure) + offset);
            *element_pnt = parse_number(case_nr, struct_name, item.key());
        }
    }
}
#pragma GCC diagnostic pop


Eigen::MatrixXd TestCaseImporter::parse_matrix(int n, std::string struct_key, std::string key){
    int rows = data["cases"][n][struct_key][key].size();
    int columns = data["cases"][n][struct_key][key][0].size();
    Eigen::MatrixXd ret = Eigen::MatrixXd(rows, columns);

    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < columns; j++) {
            ret(i, j) = data["cases"][n][struct_key][key][i][j];
        }
    }
    return ret;
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