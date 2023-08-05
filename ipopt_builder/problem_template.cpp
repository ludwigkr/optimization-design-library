#include "ProblemFormulation.h"

#include <cassert>

#ifdef __GNUC__
#pragma GCC diagnostic ignored "-Wunused-parameter"
#endif

using namespace Ipopt;

bool ProblemFormulation::get_nlp_info(Index &n, Index &m, Index &nnz_jac_g, Index &nnz_h_lag, IndexStyleEnum &index_style) {
    n = N_XOPTS;

    m = N_CONSTRAINTS;

    nnz_jac_g = CONSTRAINTS_JACOBIAN_NNZ;

    // Non-Zeros of the lagrange hessian. Don't get confused with multiple Matrices added to each other.
    // The final lagrange hessian is the result of addition of all these Matrices and only for the final
    // Matrix you count the (structural) non-zeros.
    // For symetric matrices you only count the lower triangular entries (including diagonal entries)
    nnz_h_lag = LAGRANGE_HESSIAN_NNZ;

    // We use the standard fortran index style for row/col entries
    // use the C style indexing (0-based) for the matrices
    index_style = TNLP::C_STYLE;

    return true;
}

bool ProblemFormulation::get_bounds_info(Index n, Number *x_l, Number *x_u, Index m, Number *g_l, Number *g_u) {
    // here, the n and m we gave IPOPT in get_nlp_info are passed back to us.
    // If desired, we could assert to make sure they are what we think they are.
    assert(n == N_XOPTS);
    assert(m == N_CONSTRAINTS);

    // x_l[0] = -1.0;
    // x_u[0] = 1.0;
    // x_l[0] = -1.0;
    // x_u[0] = 1.0;

    // x2 has no upper or lower bound, so we set them to
    // a large negative and a large positive number.
    // The value that is interpretted as -/+infinity can be
    // set in the options, but it defaults to -/+1e19
    //
    /* LBX PLACEHOLDER*/

    /* UBX PLACEHOLDER*/

    // g_l[0] = g_u[0] = 0.0;
    /* LBG PLACEHOLDER*/

    /* UBG PLACEHOLDER*/

    return true;
}

bool ProblemFormulation::get_starting_point(Index n, bool init_x, Number *x, bool init_z, Number *z_L, Number *z_U, Index m, bool init_lambda, Number *lambda) {
    // Here, we assume we only have starting values for x, if you code
    // your own NLP, you can provide starting values for the others if
    // you wish.
    assert(init_x == true);
    assert(init_z == false);
    assert(init_lambda == false);

    for (int i = 0; i < N_XOPTS; i++) {
        x[i] = initial_guess[i];
    }

    return true;
}

bool ProblemFormulation::eval_f(Index n, const Number *x, bool new_x, Number &obj_value) {
    // return the value of the objective function
    Number x2 = x[1];

    // obj_value = -(x[1] - 2.0) * (x[1] - 2.0);
    /* OBJECTIVE PLACEHOLDER*/

    return true;
}

bool ProblemFormulation::eval_grad_f(Index n, const Number *x, bool new_x, Number *grad_f) {
    // return the gradient of the objective function grad_{x} f(x)

    // grad_f[0] = 0.0;
    // grad_f[1] = -2.0 * (x[1] - 2.0);
    /* OBJECTIVE_JACOBIAN PLACEHOLDER*/

    return true;
}

bool ProblemFormulation::eval_g(Index n, const Number *x, bool new_x, Index m, Number *g) {
    // return the value of the constraints: g(x)

    // g[0] = -(x1 * x1 + x2 - 1.0);
    /* CONSTRAINTS PLACEHOLDER*/

    return true;
}

bool ProblemFormulation::eval_jac_g(Index n, const Number *x, bool new_x, Index m, Index nele_jac, Index *iRow, Index *jCol, Number *values) {
    if (values == NULL) {
        // return the structure of the jacobian of the constraints

        /* CONSTRAINTS_JACOBIAN_SPARSE_INDEX PLACEHOLDER*/
        // https://coin-or.github.io/Ipopt/IMPL.html#TRIPLET
        // // element at 1,1: grad_{x1} g_{1}(x)
        // iRow[0] = 1;
        // jCol[0] = 1;

        // // element at 1,2: grad_{x2} g_{1}(x)
        // iRow[1] = 1;
        // jCol[1] = 2;
    } else {

        /* CONSTRAINTS_JACOBIAN_SPARSE_VALUES PLACEHOLDER*/
        // return the values of the jacobian of the constraints
        // Number x1 = x[0];

        // // element at 1,1: grad_{x1} g_{1}(x)
        // values[0] = -2.0 * x1;

        // // element at 1,2: grad_{x1} g_{1}(x)
        // values[1] = -1.0;
    }

    return true;
}

bool ProblemFormulation::eval_h(Index n, const Number *x, bool new_x, Number obj_factor, Index m, const Number *lambda, bool new_lambda, Index nele_hess, Index *iRow, Index *jCol, Number *values) {
    if (values == NULL) {
        // return the structure. This is a symmetric matrix, fill the lower left
        // triangle only.

        /* CONSTRAINTS_JACOBIAN_SPARSE_INDEX PLACEHOLDER*/
        // // element at 1,1: grad^2_{x1,x1} L(x,lambda)
        // iRow[0] = 1;
        // jCol[0] = 1;

        // // element at 2,2: grad^2_{x2,x2} L(x,lambda)
        // iRow[1] = 2;
        // jCol[1] = 2;

        // Note: off-diagonal elements are zero for this problem
    } else {
        // return the values

        /* CONSTRAINTS_JACOBIAN_SPARSE_VALUES PLACEHOLDER*/
        // element at 1,1: grad^2_{x1,x1} L(x,lambda)
        // values[0] = -2.0 * lambda[0];

        // // element at 2,2: grad^2_{x2,x2} L(x,lambda)
        // values[1] = -2.0 * obj_factor;

        // Note: off-diagonal elements are zero for this problem
    }

    return true;
}

void ProblemFormulation::finalize_solution(SolverReturn status, Index n, const Number *x, const Number *z_L, const Number *z_U, Index m, const Number *g, const Number *lambda, Number obj_value, const IpoptData *ip_data, IpoptCalculatedQuantities *ip_cq) {
    // here is where we would store the solution to variables, or write to a file, etc
    // so we could use the solution. Since the solution is displayed to the console,
    // we currently do nothing here.
}
