#include "sqpmethod.h"
#include <chrono>
#include <iostream>
#include <eigen3/Eigen/Core>
//#define PATS_OCP_PROFILING

void SQPSolver::init(QuadraticOptimizer *qpsolver) {
    _qpsolver = qpsolver;
    _max_cpu_time = 1. / 100;
}

void SQPSolver::setup(sqp_solver_configuration _config) {
    config = _config;
    if (use_casadi) {
        std::cout << "WARNING: call SQPSolver:setup before init_casadi! Otherwise casadi will run with default parameters" << std::endl;
    }
}

#ifdef OCP_DEV
void SQPSolver::init_casadi(std::string problem_solver_path) {
    use_casadi = true;
    casadi::Dict opts;
    opts["print_time"] = false;
    opts["print_status"] =  false;
    opts["print_header"] = false;
    opts["print_iteration"] = false;
    opts["tol_pr"] = config.tol_pr;
    opts["tol_du"] = config.tol_du;
    opts["min_step_size"] = config.min_step_size;
    opts["convexify_strategy"] = "eigen-reflect"; //NONE|regularize|eigen-reflect|eigen-clip.
    opts["hessian_approximation"] = "exact"; //limited-memory|exact
    opts["max_iter"] = config.max_sqp_iterations;

    opts["qpsol"] = "qpoases";
    opts["qpsol_options.printLevel"] = "none";
    opts["qpsol_options.error_on_fail"] = false;

    // opts["qpsol"] = "osqp"; //TODO: Requires some work to install casadi with osqp

    casadi_solver = casadi::nlpsol("solver", "sqpmethod", problem_solver_path, opts);

}
#endif


double SQPSolver::l1_sum_viol(Eigen::VectorXd z, quadratic_problem_values *quad_prob_valuess) {
    double sum_viol = 0;
    uint n_optvars = quad_prob_valuess->lbx.size();
    uint n_constraints = quad_prob_valuess->ubg.size();

    for (uint i = 0; i < n_optvars; i++) {
        sum_viol += fmax(quad_prob_valuess->lbx[i] - z[i], 0);
        sum_viol += fmax(z[i] - quad_prob_valuess->ubx[i], 0);
    }
    for (uint i = 0; i < n_constraints; i++) {
        sum_viol += fmax(quad_prob_valuess->lbg[i] - z[n_optvars + i], 0);
        sum_viol += fmax(z[n_optvars + i] - quad_prob_valuess->ubg[i], 0);
    }

    return sum_viol;
}


Eigen::VectorXd SQPSolver::gradient_lagrangian(problem_solution *prob_sol, quadratic_problem_values *quad_prob_values) {
    // std::cout << "xopt: " << prob_sol->Xopt.transpose() << std::endl;
    Eigen::VectorXd gLag = _qpsolver->dJ(prob_sol->Xopt);
    // std::cout << "dJ:" << gLag.transpose() << std::endl;
    // std::cout << "lam_g:" << prob_sol.lagrange_multiplier.transpose() << std::endl;
    Eigen::MatrixXd dconstraints = _qpsolver->constraint_derivative(quad_prob_values, prob_sol);

    // std::cout << "dconstr.: " << dconstraints << std::endl;
    for (uint i = 0; i < prob_sol->constraints_val.size(); i++) {
        // std::cout << "lam_gi: " << prob_sol.lagrange_multiplier[i] * dconstraints(i, Eigen::all) << std::endl;;
        gLag += prob_sol->lagrange_multiplier[i] * dconstraints(i, Eigen::all).transpose();
        // std::cout << "gLag: " << gLag.transpose() << std::endl;
    }
    return gLag;
}

void SQPSolver::backtracking_casadi(problem_solution *prev_qpsolution, problem_solution *qpsolution, quadratic_problem_values *quad_prob_valuess) {
    sigma = fmax(sigma, qpsolution->lagrange_multiplier.cwiseAbs().maxCoeff());
    double l1_infeas = l1_sum_viol(qpsolution->Z,  quad_prob_valuess);
    Eigen::VectorXd dx = qpsolution->Xopt - prev_qpsolution->Xopt;
    Eigen::VectorXd dlam = qpsolution->lagrange_multiplier - prev_qpsolution->lagrange_multiplier;
    double tl1 = dx.transpose() * _qpsolver->dJ(prev_qpsolution->Xopt);
    double l1 = prev_qpsolution->costs + sigma * l1_infeas;
    double c1 = 1e-4;
    double beta = 0.8;
    double t = 1.;

    Eigen::VectorXd z_cand = prev_qpsolution->Z;
    double fk_cand;
    problem_solution sol_cand;
    for (uint minor_iter = 0; minor_iter < 5; minor_iter++) {
        z_cand.segment(0, prev_qpsolution->Xopt.size()) = prev_qpsolution->Xopt + t * dx;
        fk_cand = _qpsolver->costs(z_cand.segment(0, prev_qpsolution->Xopt.size()));
        // std::cout << "l1_infeas_cand: " << l1_infeas_cand << std::endl;

        double l1_cand = fk_cand + sigma * l1_sum_viol(z_cand, quad_prob_valuess);

        if (l1_cand <= l1 + t * c1 * tl1) {
            qpsolution->Xopt = prev_qpsolution->Xopt + t * dx;
            qpsolution->lagrange_multiplier = prev_qpsolution->lagrange_multiplier + t * dlam;
            return;
        } else {
            t *= beta;
        }
    }

    return;
}

Eigen::VectorXd SQPSolver::solve_line_search(quadratic_problem_values *quad_prob_values) {
    Eigen::VectorXd X0 = quad_prob_values->X0;
    problem_solution prev_qpsolution(quad_prob_values, _qpsolver->constraints(quad_prob_values->X0, quad_prob_values->param));
    problem_solution qpsolution = prev_qpsolution;
    std::chrono::_V2::system_clock::time_point t_start = std::chrono::high_resolution_clock::now();
    std::chrono::_V2::system_clock::time_point t_now;
    double cpu_time_passed;
    sigma = 0;
    // _qpsolver->print_eigenvector("X0", quad_prob_values->X0.transpose());

    for (int iteration = 0; iteration <= config.max_sqp_iterations; iteration++) {

        Eigen::VectorXd gLag = gradient_lagrangian(&qpsolution, quad_prob_values);
        double du_inf = gLag.cwiseAbs().maxCoeff();

        double pr_inf = l1_sum_viol(qpsolution.Z, quad_prob_values);

        double dx_inf = std::numeric_limits<double>::infinity();
        if (iteration > 0)
            dx_inf = (qpsolution.Xopt - prev_qpsolution.Xopt).cwiseAbs().maxCoeff();

        // std::cout << "iter: " << iteration << " x[0]: " << qpsolution.Xopt[0] << " lamg[0]: " << qpsolution.lagrange_multiplier[0]
        //           << " pr_inf: " << pr_inf << " du_inf: " << du_inf << " dx_inf: " << dx_inf << std::endl;

        if (iteration > 0) {
            if (iteration >= min_iterations && pr_inf < config.tol_pr && du_inf < config.tol_du) { // solver converged
                return return_xopt(qpsolution.Xopt, X0);
            }
            if (iteration >= min_iterations && dx_inf < config.min_step_size) {// solver doesn't make progress

                return return_xopt(qpsolution.Xopt, X0);
            }
        }

        prev_qpsolution = qpsolution;
        quad_prob_values->X0 = qpsolution.Xopt;

        if (_max_cpu_time > 0) {
            t_now = std::chrono::high_resolution_clock::now();
            cpu_time_passed = std::chrono::duration_cast<std::chrono::microseconds>(t_now - t_start).count() * 1e-6;
            if (cpu_time_passed > _max_cpu_time) {
                // std::cout << "WARNING: SQP stops because it gets late..." << std::endl;
                return qpsolution.Xopt;
            }
            cpu_time_remaining = _max_cpu_time - cpu_time_passed;
            if (cpu_time_remaining < 0.001) {
                // std::cout << "WARNING: SQP stops not enough time is left for another QP iteration." << std::endl;
                return return_xopt(qpsolution.Xopt, X0);
            }
        } else {
            cpu_time_remaining = 0;
        }

        if (iteration == 0) {
            qpsolution = _qpsolver->solve(quad_prob_values, &prev_qpsolution, true, cpu_time_remaining);
        }
        else {
            qpsolution = _qpsolver->solve(quad_prob_values, &prev_qpsolution, false, cpu_time_remaining);
            backtracking_casadi(&prev_qpsolution, &qpsolution, quad_prob_values);
        }
#if OPTI_ROSVIS
        _ros_interface->path(_qpsolver->trajectory(qpsolution.Xopt, state_trajectory_t), opti_current_guess);
        _ros_interface->state_trajectory(_qpsolver->trajectory(qpsolution.Xopt, state_trajectory_t));
        _ros_interface->input_trajectory(_qpsolver->trajectory(qpsolution.Xopt, state_trajectory_t), _qpsolver->trajectory(qpsolution.Xopt, input_trajectory_t), drone_input_trajectory);
        _ros_interface->input_trajectory(_qpsolver->trajectory(qpsolution.Xopt, state_trajectory_t), _qpsolver->trajectory(qpsolution.Xopt, virtual_input_trajectory_t), drone_virtual_input_trajectory);
        _ros_interface->publish();
#endif
        // _qpsolver->print_eigenvector("X", qpsolution.Xopt);


        if (qpsolution.status != 0 && iteration == 0) {
            // std::cout << "WARNING: Quadratic solver is complaining in initial iteration! return status " << qpsolution.status << std::endl;
            return Eigen::VectorXd(prev_qpsolution.Xopt.size()).setZero();
        } else if (qpsolution.status != 0) {
            // std::cout << "WARNING: Quadratic solver is complaining after some iterations! return status " << qpsolution.status << std::endl;
            return return_xopt(prev_qpsolution.Xopt, X0);
        }
    }

    return return_xopt(qpsolution.Xopt, X0);
}


#ifdef OCP_DEV
Eigen::VectorXd SQPSolver::solve_casadi(quadratic_problem_values *quad_prob_values) {
    Eigen::VectorXd eigXopt(quad_prob_values->X0.size());
    eigXopt.setZero();

    if (use_casadi) {
        arg["x0"] = std::vector<double>(quad_prob_values->X0.data(), quad_prob_values->X0.data() + quad_prob_values->X0.size());;
        arg["lbx"] = std::vector<double>(quad_prob_values->lbx.data(), quad_prob_values->lbx.data() + quad_prob_values->lbx.size());
        arg["ubx"] = std::vector<double>(quad_prob_values->ubx.data(), quad_prob_values->ubx.data() + quad_prob_values->ubx.size());
        arg["lbg"] = std::vector<double>(quad_prob_values->lbg.data(), quad_prob_values->lbg.data() + quad_prob_values->lbg.size());
        arg["ubg"] = std::vector<double>(quad_prob_values->ubg.data(), quad_prob_values->ubg.data() + quad_prob_values->ubg.size());
        arg["p"] = std::vector<double>(quad_prob_values->param.data(), quad_prob_values->param.data() + quad_prob_values->param.size());
        res = casadi_solver(arg);

        std::vector<double> opti_var = std::vector<double>(res.at("x"));
        // std::cout << "Casadi Xopt: " << res.at("x") << std::endl;

        eigXopt = Eigen::Map<Eigen::VectorXd>(&(opti_var.at(0)), opti_var.size());

        return eigXopt;
    } else {
        std::cout << "WARNING: casadi not initialized" << std::endl;
        return eigXopt;
    }
}

#endif

Eigen::VectorXd SQPSolver::return_xopt(Eigen::VectorXd Xopt, Eigen::VectorXd X0) {
    // Safety check to ensure that the optimizer was actually called. If the result hasn't changed (optimizer hasn't called) return 0 vector.
    if ((Xopt - X0).norm() > 0)
        return Xopt;
    else {
        std::cout << "SQPSolver: Return_xopt has set xopt to 0." << std::endl;
        return Xopt.setZero();
    }
}

std::ostream &operator<<(std::ostream &os, sqp_solver_configuration &sqp_config) {
    os << "sqp_max_iterations: " << sqp_config.max_sqp_iterations << ", tol_pr: " << sqp_config.tol_pr << ", tol_du: " << sqp_config.tol_du
       << ", min_step_size: " << sqp_config.min_step_size;
    return os;
}
