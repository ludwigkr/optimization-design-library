
#include <tuple>
#include <fstream>
#include <eigen3/Eigen/Core>
#include "nlohmann/json.hpp"

struct scenario_parameter;
struct problem_parameter;
struct optimized_variable;

using json = nlohmann::json;

class TestCaseImporter{

    public:
        TestCaseImporter(std::string s) {
            filepath = s;
        }

        void load_json();
        void test_cast(int n, scenario_parameter* scenrio, problem_parameter* prob_param, optimized_variable* xopt);
        uint amount_cases() {return data.size();};

    private:
        std::string filepath;
        json data; 
        int N = 0;

        Eigen::VectorXd parse_vector(int n, std::string struct_key, std::string key);
        float parse_number(int n, std::string struct_key, std::string key);
};