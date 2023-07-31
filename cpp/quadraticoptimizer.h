#pragma once
#include <vector>
#include <iostream>
#include <eigen3/Eigen/Core>
#include <limits>


struct quadratic_problem_values {
    Eigen::VectorXd X0;
    Eigen::VectorXd lbg;
    Eigen::VectorXd ubg;
    Eigen::VectorXd lbx;
    Eigen::VectorXd ubx;
    Eigen::VectorXd param;

    quadratic_problem_values() {
        X0 = {};
        lbg = {};
        ubg = {};
        lbx = {};
        ubx = {};
        param = {};
    }

    quadratic_problem_values(Eigen::VectorXd _X0, Eigen::VectorXd _lbg, Eigen::VectorXd _ubg, Eigen::VectorXd _lbx, Eigen::VectorXd _ubx, Eigen::VectorXd _param): X0(_X0), lbg(_lbg), ubg(_ubg), lbx(_lbx), ubx(_ubx), param(_param) {};

    quadratic_problem_values(int n_optvars, int n_constraints, int n_params) {
        X0 = Eigen::VectorXd(n_optvars).setZero();
        lbg = Eigen::VectorXd(n_constraints).setZero();
        ubg = Eigen::VectorXd(n_constraints).setZero();
        ubx = Eigen::VectorXd(n_optvars).setZero();
        lbx = Eigen::VectorXd(n_optvars).setZero();
        param  = Eigen::VectorXd(n_params).setZero();
    }
};

struct problem_solution {
    Eigen::VectorXd Xopt;
    Eigen::VectorXd constraints_val;
    Eigen::VectorXd lagrange_multiplier;
    Eigen::VectorXd Z;
    double costs;
    int status;

    problem_solution() {
        Xopt = {};
        constraints_val = {};
        lagrange_multiplier = {};
        costs = std::numeric_limits<double>::infinity();
        status = -1;
        Z = {};
    };
    problem_solution(Eigen::VectorXd xopt, Eigen::VectorXd consts, Eigen::VectorXd _lagrange, double objval, int s): Xopt(xopt), constraints_val(consts), lagrange_multiplier(_lagrange), costs(objval), status(s) {
        Z = Eigen::VectorXd(xopt.size() + consts.size());
        Z.segment(0, xopt.size()) = xopt;
        Z.segment(xopt.size(), consts.size()) = consts;
    };

    problem_solution(quadratic_problem_values *quad_prob_values, Eigen::VectorXd _constraints_val) {
        int n_optvars = quad_prob_values->X0.size();
        int n_constraints = quad_prob_values->lbg.size();
        Xopt = quad_prob_values->X0;
        constraints_val = _constraints_val;
        lagrange_multiplier = Eigen::VectorXd(n_constraints).setZero();
        Z = Eigen::VectorXd(n_optvars + n_constraints).setZero();
        Z.segment(0, n_optvars) = quad_prob_values->X0;
        Z.segment(n_optvars, n_constraints) = _constraints_val;
        status = -1;
    };
};

enum trajectory_type {
    state_trajectory_t,
    input_trajectory_t,
    virtual_input_trajectory_t,
};

struct scenario_parameter;
struct problem_parameter;

class QuadraticOptimizer {
public:
    virtual void init() = 0;
    virtual Eigen::VectorXd constraints(quadratic_problem_values *quad_prob_valuess, problem_solution *prev_qpsolution) = 0;
    virtual Eigen::VectorXd constraints(Eigen::VectorXd xopt, Eigen::VectorXd param) = 0;
    virtual Eigen::MatrixXd constraint_derivative(quadratic_problem_values *quad_prob_valuess, problem_solution *prev_qpsolution) = 0;
    virtual problem_solution solve(quadratic_problem_values *quad_prob_valuess, bool init, double cpu_time) = 0;
    virtual problem_solution solve(quadratic_problem_values *quad_prob_valuess, problem_solution *prev_qpsolution, bool init, double cpu_time) = 0;
    virtual std::string status_return_name(int status) = 0;
    virtual std::string quadratic_solver_library() = 0;

    virtual Eigen::VectorXd parameter(problem_parameter *prob_param, scenario_parameter *scenerio) = 0;
    virtual Eigen::VectorXd initial_guess(problem_parameter *prob_param, scenario_parameter *scenerio) = 0;
    virtual Eigen::VectorXd ubx(problem_parameter *prob_param, scenario_parameter *scenerio) = 0;
    virtual Eigen::VectorXd lbx(problem_parameter *prob_param, scenario_parameter *scenerio) = 0;
    virtual Eigen::VectorXd ubg(problem_parameter *prob_param, scenario_parameter *scenerio) = 0;
    virtual Eigen::VectorXd lbg(problem_parameter *prob_param, scenario_parameter *scenerio) = 0;

    double costs(Eigen::VectorXd X) {
        auto ret = 0.5 * X.transpose() * _H * X + X.transpose() * _g;
        return ret[0];
    };

    Eigen::VectorXd dJ(Eigen::VectorXd X) {
        return _H * X + _g;
    }

    void print_eigenvector(std::string name, Eigen::VectorXd vec) {
        if (vec.size() > 0) {
            std::cout << name << ": [";

            for (uint k = 0; k < vec.size() - 1; k++)
                std::cout << vec[k] << ", ";
            std::cout << vec[vec.size() - 1] << "]" << std::endl;
        }
    }

    template<class T>
    void print_array(std::string name, long long int n, T *vec) {
        std::cout << name << ": [";
        for (long long int k = 0; k < n - 1; k++)
            std::cout << vec[k] << ", ";
        std::cout << vec[n - 1] << "]" << std::endl;
    }

    void print_vector(std::string name, std::vector<float> vec) {
        std::cout << name << ": [";
        for (long unsigned int k = 0; k < vec.size() - 1; k++)
            std::cout << vec[k] << ", ";
        std::cout << vec[vec.size() - 1] << "]" << std::endl;
    }

    void print_quadratic_problem_design(quadratic_problem_values quad_prob_valuess, problem_solution prob_sol) {
        std::cout << "***********Problem optimization step (PATS):**************" << std::endl;
        print_eigenvector("idx", Eigen::VectorXd::LinSpaced(quad_prob_valuess.X0.size(), 0, quad_prob_valuess.X0.size() - 1));
        print_eigenvector("X0", quad_prob_valuess.X0);
        print_eigenvector("lbx", quad_prob_valuess.lbx);
        print_eigenvector("ubx", quad_prob_valuess.ubx);
        print_eigenvector("Xopt", prob_sol.Xopt);

        print_eigenvector("lbg", quad_prob_valuess.lbg);
        print_eigenvector("g(x0)", constraints(quad_prob_valuess.X0, quad_prob_valuess.param));
        print_eigenvector("ubg", quad_prob_valuess.ubg);
        print_eigenvector("lam", prob_sol.lagrange_multiplier);
        print_eigenvector("param", quad_prob_valuess.param);
        std::cout << "solver_status: " << status_return_name(prob_sol.status) << " (" << prob_sol.status << ")" << std::endl;
        std::cout << "*******************************************" << std::endl;

    }

    Eigen::MatrixXd hessian() {
        return _H;
    }

protected:
    Eigen::MatrixXd _H;
    Eigen::VectorXd _g;
};
