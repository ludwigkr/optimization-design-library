#include "formulation_problem_ipopt.h"

#include <cassert>

#ifdef __GNUC__
#pragma GCC diagnostic ignored "-Wunused-parameter"
#endif

/* MAPPERS PLACEHOLDER*/

/* OS STREAM PLACEHOLDER*/

/* OPERATORS PLACEHOLDER*/

using namespace Ipopt;

bool ProblemFormulation::get_nlp_info(Index &n, Index &m, Index &nnz_jac_g, Index &nnz_h_lag, IndexStyleEnum &index_style) {
    n = N_XOPTS;
    m = N_CONSTRAINTS;
    nnz_jac_g = CONSTRAINTS_JACOBIAN_NNZ;
    nnz_h_lag = LAGRANGE_HESSIAN_NNZ;
    index_style = TNLP::C_STYLE;

    return true;
}

bool ProblemFormulation::get_bounds_info(Index n, Number *x_l, Number *x_u, Index m, Number *g_l, Number *g_u) {
    assert(n == N_XOPTS);
    assert(m == N_CONSTRAINTS);
    assert(scenario != nullptr);
    assert(prob_param != nullptr);

    Number *lbx = x_l;
    Number *ubx = x_u;
    Number *lbg = g_l;
    Number *ubg = g_u;

    /* LBX PLACEHOLDER*/

    /* UBX PLACEHOLDER*/

    /* LBG PLACEHOLDER*/

    /* UBG PLACEHOLDER*/

    return true;
}

bool ProblemFormulation::get_starting_point(Index n, bool init_x, Number *x, bool init_z, Number *z_L, Number *z_U, Index m, bool init_lambda, Number *lambda) {
    assert(init_x == true);
    assert(init_z == false);
    assert(init_lambda == false);

    /* INITIAL_GUESS PLACEHOLDER*/

    return true;
}

bool ProblemFormulation::eval_f(Index n, const Number *x, bool new_x, Number &obj_value) {
    assert(scenario != nullptr);
    assert(prob_param != nullptr);
    const Number *xopt = x;

    /* OBJECTIVE PLACEHOLDER*/

    return true;
}

bool ProblemFormulation::eval_grad_f(Index n, const Number *x, bool new_x, Number *grad_f) {
    assert(scenario != nullptr);
    assert(prob_param != nullptr);
    const Number *xopt = x;

    /* OBJECTIVE_JACOBIAN PLACEHOLDER*/

    return true;
}

bool ProblemFormulation::eval_g(Index n, const Number *x, bool new_x, Index m, Number *g) {
    assert(scenario != nullptr);
    assert(prob_param != nullptr);
    const Number *xopt = x;

    /* CONSTRAINTS PLACEHOLDER*/

    return true;
}

bool ProblemFormulation::eval_jac_g(Index n, const Number *x, bool new_x, Index m, Index nele_jac, Index *iRow, Index *jCol, Number *values) {
    assert(scenario != nullptr);
    assert(prob_param != nullptr);
    const Number *xopt = x;
    if (values == NULL) {
        /* CONSTRAINTS_JACOBIAN_SPARSE_INDEX PLACEHOLDER*/
    } else {

        /* CONSTRAINTS_JACOBIAN_SPARSE_VALUES PLACEHOLDER*/
    }

    return true;
}

bool ProblemFormulation::eval_h(Index n, const Number *x, bool new_x, Number obj_factor, Index m, const Number *lambda, bool new_lambda, Index nele_hess, Index *iRow, Index *jCol, Number *values) {
    assert(scenario != nullptr);
    assert(prob_param != nullptr);
    if (values == NULL) {

        /* LAGRANGIAN_HESSIAN_SPARSE_INDEX PLACEHOLDER*/
    } else {
        const Number *xopt = x;
        const Number *lamg = lambda;

        /* LAGRANGIAN_HESSIAN_SPARSE_VALUES PLACEHOLDER*/
    }

    return true;
}

void ProblemFormulation::finalize_solution(SolverReturn status, Index n, const Number *x, const Number *z_L, const Number *z_U, Index m, const Number *g, const Number *lambda, Number obj_value, const IpoptData *ip_data, IpoptCalculatedQuantities *ip_cq) {
    /*WRITE BACK SOLUTION PLACEHOLDER*/
}

