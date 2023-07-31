#include "problem_index.h"
#include "solvertemplate.h"

[[maybe_unused]] static const char *qpoases_status_names[] = {
    "TERMINAL_LIST_ELEMENT",
    "SUCCESSFUL_RETURN",
    "RET_DIV_BY_ZERO",
    "RET_INDEX_OUT_OF_BOUNDS",
    "RET_INVALID_ARGUMENTS",
    "RET_ERROR_UNDEFINED",
    "RET_WARNING_UNDEFINED",
    "RET_INFO_UNDEFINED",
    "RET_EWI_UNDEFINED",
    "RET_AVAILABLE_WITH_LINUX_ONLY",
    "RET_UNKNOWN_BUG",
    "RET_PRINTLEVEL_CHANGED",
    "RET_NOT_YET_IMPLEMENTED",
    "RET_INDEXLIST_MUST_BE_REORDERD",
    "RET_INDEXLIST_EXCEEDS_MAX_LENGTH",
    "RET_INDEXLIST_CORRUPTED",
    "RET_INDEXLIST_OUTOFBOUNDS",
    "RET_INDEXLIST_ADD_FAILED",
    "RET_INDEXLIST_INTERSECT_FAILED",
    "RET_INDEX_ALREADY_OF_DESIRED_STATUS",
    "RET_ADDINDEX_FAILED",
    "RET_REMOVEINDEX_FAILED",
    "RET_SWAPINDEX_FAILED",
    "RET_NOTHING_TO_DO",
    "RET_SETUP_BOUND_FAILED",
    "RET_SETUP_CONSTRAINT_FAILED",
    "RET_MOVING_BOUND_FAILED",
    "RET_MOVING_CONSTRAINT_FAILED",
    "RET_SHIFTING_FAILED",
    "RET_ROTATING_FAILED",
    "RET_QPOBJECT_NOT_SETUP",
    "RET_QP_ALREADY_INITIALISED",
    "RET_NO_INIT_WITH_STANDARD_SOLVER",
    "RET_RESET_FAILED",
    "RET_INIT_FAILED",
    "RET_INIT_FAILED_TQ",
    "RET_INIT_FAILED_CHOLESKY",
    "RET_INIT_FAILED_HOTSTART",
    "RET_INIT_FAILED_INFEASIBILITY",
    "RET_INIT_FAILED_UNBOUNDEDNESS",
    "RET_INIT_FAILED_REGULARISATION",
    "RET_INIT_SUCCESSFUL",
    "RET_OBTAINING_WORKINGSET_FAILED",
    "RET_SETUP_WORKINGSET_FAILED",
    "RET_SETUP_AUXILIARYQP_FAILED",
    "RET_NO_CHOLESKY_WITH_INITIAL_GUESS",
    "RET_NO_EXTERN_SOLVER",
    "RET_QP_UNBOUNDED",
    "RET_QP_INFEASIBLE",
    "RET_QP_NOT_SOLVED",
    "RET_QP_SOLVED",
    "RET_UNABLE_TO_SOLVE_QP",
    "RET_INITIALISATION_STARTED",
    "RET_HOTSTART_FAILED",
    "RET_HOTSTART_FAILED_TO_INIT",
    "RET_HOTSTART_FAILED_AS_QP_NOT_INITIALISED",
    "RET_ITERATION_STARTED",
    "RET_SHIFT_DETERMINATION_FAILED",
    "RET_STEPDIRECTION_DETERMINATION_FAILED",
    "RET_STEPLENGTH_DETERMINATION_FAILED",
    "RET_OPTIMAL_SOLUTION_FOUND",
    "RET_HOMOTOPY_STEP_FAILED",
    "RET_HOTSTART_STOPPED_INFEASIBILITY",
    "RET_HOTSTART_STOPPED_UNBOUNDEDNESS",
    "RET_WORKINGSET_UPDATE_FAILED",
    "RET_MAX_NWSR_REACHED",
    "RET_CONSTRAINTS_NOT_SPECIFIED",
    "RET_INVALID_FACTORISATION_FLAG",
    "RET_UNABLE_TO_SAVE_QPDATA",
    "RET_STEPDIRECTION_FAILED_TQ",
    "RET_STEPDIRECTION_FAILED_CHOLESKY",
    "RET_CYCLING_DETECTED",
    "RET_CYCLING_NOT_RESOLVED",
    "RET_CYCLING_RESOLVED",
    "RET_STEPSIZE",
    "RET_STEPSIZE_NONPOSITIVE",
    "RET_SETUPSUBJECTTOTYPE_FAILED",
    "RET_ADDCONSTRAINT_FAILED",
    "RET_ADDCONSTRAINT_FAILED_INFEASIBILITY",
    "RET_ADDBOUND_FAILED",
    "RET_ADDBOUND_FAILED_INFEASIBILITY",
    "RET_REMOVECONSTRAINT_FAILED",
    "RET_REMOVEBOUND_FAILED",
    "RET_REMOVE_FROM_ACTIVESET",
    "RET_ADD_TO_ACTIVESET",
    "RET_REMOVE_FROM_ACTIVESET_FAILED",
    "RET_ADD_TO_ACTIVESET_FAILED",
    "RET_CONSTRAINT_ALREADY_ACTIVE",
    "RET_ALL_CONSTRAINTS_ACTIVE",
    "RET_LINEARLY_DEPENDENT",
    "RET_LINEARLY_INDEPENDENT",
    "RET_LI_RESOLVED",
    "RET_ENSURELI_FAILED",
    "RET_ENSURELI_FAILED_TQ",
    "RET_ENSURELI_FAILED_NOINDEX",
    "RET_ENSURELI_FAILED_CYCLING",
    "RET_BOUND_ALREADY_ACTIVE",
    "RET_ALL_BOUNDS_ACTIVE",
    "RET_CONSTRAINT_NOT_ACTIVE",
    "RET_BOUND_NOT_ACTIVE",
    "RET_HESSIAN_NOT_SPD",
    "RET_HESSIAN_INDEFINITE",
    "RET_MATRIX_SHIFT_FAILED",
    "RET_MATRIX_FACTORISATION_FAILED",
    "RET_PRINT_ITERATION_FAILED",
    "RET_NO_GLOBAL_MESSAGE_OUTPUTFILE",
    "RET_DISABLECONSTRAINTS_FAILED",
    "RET_ENABLECONSTRAINTS_FAILED",
    "RET_ALREADY_ENABLED",
    "RET_ALREADY_DISABLED",
    "RET_NO_HESSIAN_SPECIFIED",
    "RET_USING_REGULARISATION",
    "RET_EPS_MUST_BE_POSITVE",
    "RET_REGSTEPS_MUST_BE_POSITVE",
    "RET_HESSIAN_ALREADY_REGULARISED",
    "RET_CANNOT_REGULARISE_IDENTITY",
    "RET_CANNOT_REGULARISE_SPARSE",
    "RET_NO_REGSTEP_NWSR",
    "RET_FEWER_REGSTEPS_NWSR",
    "RET_CHOLESKY_OF_ZERO_HESSIAN",
    "RET_ZERO_HESSIAN_ASSUMED",
    "RET_CONSTRAINTS_ARE_NOT_SCALED",
    "RET_INITIAL_BOUNDS_STATUS_NYI",
    "RET_ERROR_IN_CONSTRAINTPRODUCT",
    "RET_FIX_BOUNDS_FOR_LP",
    "RET_USE_REGULARISATION_FOR_LP",
    "RET_UPDATEMATRICES_FAILED",
    "RET_UPDATEMATRICES_FAILED_AS_QP_NOT_SOLVED",
    "RET_UNABLE_TO_OPEN_FILE",
    "RET_UNABLE_TO_WRITE_FILE",
    "RET_UNABLE_TO_READ_FILE",
    "RET_FILEDATA_INCONSISTENT",
    "RET_OPTIONS_ADJUSTED",
    "RET_UNABLE_TO_ANALYSE_QPROBLEM",
    "RET_NWSR_SET_TO_ONE",
    "RET_UNABLE_TO_READ_BENCHMARK",
    "RET_BENCHMARK_ABORTED",
    "RET_INITIAL_QP_SOLVED",
    "RET_QP_SOLUTION_STARTED",
    "RET_BENCHMARK_SUCCESSFUL",
    "RET_NO_DIAGONA",
    "L_AVAILABLE",
    "RET_DIAGONAL_NOT_INITIALISED",
    "RET_ENSURELI_DROPPED",
    "RET_KKT_MATRIX_SINGULAR",
    "RET_QR_FACTORISATION_FAILED",
    "RET_INERTIA_CORRECTION_FAILED",
    "RET_NO_SPARSE_SOLVER",
    "RET_SIMPLE_STATUS_P1",
    "RET_SIMPLE_STATUS_P0",
    "RET_SIMPLE_STATUS_M1",
    "RET_SIMPLE_STATUS_M2",
    "RET_SIMPLE_STATUS_M3"
};

void SolverTemplate::init() {
    solver = SQProblem(N_XOPTS, N_CONSTRAINTS);
    Options options;
    // options.setToDefault();
    options.setToReliable();
    options.printLevel = PL_NONE;
    // options.enableRegularisation = BT_TRUE;
    Eigen::VectorXd xopt = Eigen::VectorXd(N_XOPTS).setZero();
    Eigen::VectorXd param = Eigen::VectorXd(N_PARAMS).setZero();
    solver.setOptions(options);
    memset(H, 0, sizeof(H));
    Eigen::VectorXd lamg = Eigen::VectorXd(N_CONSTRAINTS).setZero();
    /* INIT H PLACEHOLDER*/
    memset(g, 0, sizeof(g));
    /* INIT g PLACEHOLDER*/
    _H = Eigen::Map<Eigen::Matrix<double, N_XOPTS, N_XOPTS, Eigen::RowMajor>>(H);
    _g = Eigen::Map<Eigen::VectorXd>(g, N_XOPTS);
}

void SolverTemplate::qp_setup(QPSettings qpsettings [[maybe_unused]]) {}

Eigen::VectorXd SolverTemplate::constraints(quadratic_problem_values *quad_prob_values, problem_solution *prev_qpsolution) {
    Eigen::VectorXd xopt = prev_qpsolution->Xopt;
    Eigen::VectorXd param = quad_prob_values->param;
    return constraints(xopt, param);
}

Eigen::VectorXd SolverTemplate::constraints(Eigen::VectorXd xopt, Eigen::VectorXd param [[maybe_unused]]) {
    Eigen::VectorXd constraints = Eigen::VectorXd(N_CONSTRAINTS).setZero();
    /* CONSTRAINTS PLACEHOLDER*/
    return constraints;
}

Eigen::MatrixXd SolverTemplate::constraint_derivative(quadratic_problem_values *quad_prob_values, problem_solution *prev_qpsolution) {
    Eigen::VectorXd xopt = prev_qpsolution->Xopt;
    Eigen::VectorXd param = quad_prob_values->param;
    Eigen::MatrixXd dconstraints =
        Eigen::MatrixXd(N_CONSTRAINTS, N_XOPTS).setZero();
    /* CONSTRAINT_DERIVATIVES PLACEHOLDER*/
    return dconstraints;
}

Eigen::VectorXd SolverTemplate::initial_guess(problem_parameter *prob_param [[maybe_unused]], scenario_parameter *scenario [[maybe_unused]]) {
    Eigen::VectorXd initial_guess = Eigen::VectorXd(N_XOPTS).setZero();
    /* INITIAL_GUESS PLACEHOLDER*/
    return initial_guess;
}

Eigen::VectorXd SolverTemplate::parameter(problem_parameter *prob_param [[maybe_unused]], scenario_parameter *scenario [[maybe_unused]]) {
    Eigen::VectorXd parameters = Eigen::VectorXd(N_PARAMS).setZero();
    /* PARAMS PLACEHOLDER*/
    return parameters;
}

Eigen::VectorXd SolverTemplate::lbx(problem_parameter *prob_param [[maybe_unused]], scenario_parameter *scenario [[maybe_unused]]) {
    Eigen::VectorXd lbx = Eigen::VectorXd(N_XOPTS).setZero();
    /* LBX PLACEHOLDER*/
    return lbx;
}

Eigen::VectorXd SolverTemplate::ubx(problem_parameter *prob_param [[maybe_unused]], scenario_parameter *scenario [[maybe_unused]]) {
    Eigen::VectorXd ubx = Eigen::VectorXd(N_XOPTS).setZero();
    /* UBX PLACEHOLDER*/
    return ubx;
}

Eigen::VectorXd SolverTemplate::lbg(problem_parameter *prob_param [[maybe_unused]], scenario_parameter *scenario [[maybe_unused]]) {
    Eigen::VectorXd lbg = Eigen::VectorXd(N_CONSTRAINTS).setZero();
    /* LBG PLACEHOLDER*/
    return lbg;
}

Eigen::VectorXd SolverTemplate::ubg(problem_parameter *prob_param [[maybe_unused]], scenario_parameter *scenario [[maybe_unused]]) {
    Eigen::VectorXd ubg = Eigen::VectorXd(N_CONSTRAINTS).setZero();
    /* UBG PLACEHOLDER*/
    return ubg;
}

void SolverTemplate::update_matrix_H(quadratic_problem_values *quad_prob_values, problem_solution *prev_qpsolution) {
    Eigen::VectorXd xopt = prev_qpsolution->Xopt;
    Eigen::VectorXd param = quad_prob_values->param;
    Eigen::VectorXd lamg = prev_qpsolution->lagrange_multiplier;
    /* UPDATE H PLACEHOLDER*/
}

void SolverTemplate::update_vector_g(quadratic_problem_values *quad_prob_values, problem_solution *prev_qpsolution) {
    Eigen::VectorXd xopt = prev_qpsolution->Xopt;
    Eigen::VectorXd param = quad_prob_values->param;
    /* UPDATE g PLACEHOLDER*/
}

void SolverTemplate::update_matrix_A(quadratic_problem_values *quad_prob_values, problem_solution *prev_qpsolution) {
    Eigen::VectorXd xopt = prev_qpsolution->Xopt;
    Eigen::VectorXd param = quad_prob_values->param;
    /* UPDATE A PLACEHOLDER*/
}

void SolverTemplate::update_vectors_bA(quadratic_problem_values *quad_prob_values [[maybe_unused]], problem_solution *prev_qpsolution) {
    Eigen::VectorXd lbg = quad_prob_values->lbg;
    Eigen::VectorXd ubg = quad_prob_values->ubg;
    Eigen::VectorXd param = quad_prob_values->param;

    /* UPDATE bA PLACEHOLDER*/

    for (uint i = 0; i < N_CONSTRAINTS; i++) {
        ubA[i] -= prev_qpsolution->Z[N_XOPTS + i];
        lbA[i] -= prev_qpsolution->Z[N_XOPTS + i];
    }
}

void SolverTemplate::update_vectors_bx(quadratic_problem_values *quad_prob_values, problem_solution *prev_qpsolution) {
    for (uint lbxk = 0; lbxk < quad_prob_values->lbx.size(); lbxk++) {
        lb[lbxk] = quad_prob_values->lbx[lbxk] - prev_qpsolution->Xopt[lbxk];
    }

    for (uint ubxk = 0; ubxk < quad_prob_values->ubx.size(); ubxk++) {
        ub[ubxk] = quad_prob_values->ubx[ubxk] - prev_qpsolution->Xopt[ubxk];
    }
}

problem_solution SolverTemplate::solve(quadratic_problem_values *quad_prob_values, bool init, double cpu_time) {
    problem_solution prev_qpsolution(quad_prob_values, constraints(quad_prob_values->X0, quad_prob_values->param));
    return solve(quad_prob_values, &prev_qpsolution, init, cpu_time);
}

problem_solution SolverTemplate::solve(quadratic_problem_values *quad_prob_values, problem_solution *prev_qpsolution, bool init, double cpu_time) {
    update_matrix_H(quad_prob_values, prev_qpsolution);
    update_vector_g(quad_prob_values, prev_qpsolution);
    update_matrix_A(quad_prob_values, prev_qpsolution);
    update_vectors_bA(quad_prob_values, prev_qpsolution);
    update_vectors_bx(quad_prob_values, prev_qpsolution);
    int solver_status;
    int nwsr = 5 * (N_XOPTS + N_CONSTRAINTS);

    if (cpu_time > 0)
        _cpu_time = &cpu_time;
    else
        _cpu_time = nullptr;

    if (!solver.isInitialised() || init)
        solver_status = solver.init(H, g, A, lb, ub, lbA, ubA, nwsr, _cpu_time);
    else
        solver_status = solver.hotstart(H, g, A, lb, ub, lbA, ubA, nwsr, _cpu_time);

    real_t primal[N_XOPTS];
    solver.getPrimalSolution(primal);
    Eigen::VectorXd xopt =
        prev_qpsolution->Xopt + Eigen::Map<Eigen::VectorXd>(primal, N_XOPTS);
    real_t _dual[N_XOPTS + N_CONSTRAINTS];
    solver.getDualSolution(_dual);
    Eigen::VectorXd lagrange_multiplier =
        -Eigen::Map<Eigen::VectorXd>(&(_dual[N_XOPTS]), N_CONSTRAINTS);
    problem_solution ret =
        problem_solution(xopt, constraints(xopt, quad_prob_values->param),
                         lagrange_multiplier, solver.getObjVal(), solver_status);

    if (qp_return_status(ret.status)) {
        print_quadratic_problem_design(*quad_prob_values, ret);
    }

    ret.status = qp_return_status(ret.status);
    // print_quadratic_problem(primal, _dual);
    // print_array("H", N_XOPTS * N_XOPTS, H);
    return ret;
}

// std::vector<Eigen::VectorXd> SolverTemplate::trajectory(Eigen::VectorXd xopt,
// trajectory_type traj_type) {

//       std::vector<Eigen::VectorXd> traj;

//       if (traj_type == state_trajectory_t) {
//           for (uint k = 0; k <= n_steps; k++) {
//               Eigen::VectorXd sample = Eigen::VectorXd(N_DRONE_STATES);
//               for (uint i = 0; i < N_DRONE_STATES; i++) {
//                   sample[i] = xopt[state_trajectory_first + k *
//                   N_DRONE_STATES + i];
//               }
//               traj.push_back(sample);
//           }
//       } else if (traj_type == input_trajectory_t) {
//           for (uint k = 0; k < n_steps; k++) {
//               Eigen::VectorXd sample = Eigen::VectorXd(N_DRONE_INPUTS);
//               for (uint i = 0; i < N_DRONE_INPUTS; i++) {
//                   sample[i] = xopt[input_trajectory_first + k *
//                   N_DRONE_INPUTS + i];
//               }
//               traj.push_back(sample);
//           }
//       } else if (traj_type == virtual_input_trajectory_t) {
//           for (uint k = 0; k <= n_steps; k++) {
//               Eigen::VectorXd sample = Eigen::VectorXd(N_DRONE_INPUTS);
//               for (uint i = 0; i < N_DRONE_INPUTS; i++) {
//                   sample[i] = xopt[virtual_input_trajectory_first + k *
//                   N_DRONE_STATES + i];
//               }
//               traj.push_back(sample);
//           }
//       }

//       return traj;
// }

std::string SolverTemplate::status_return_name(int status) {
    return qpoases_status_names[status + 1];
};
