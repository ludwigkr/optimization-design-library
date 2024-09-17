#include <math.h>
#include <iostream>
#include "problem_formulation.hpp"


/**@input: result: Target vector for the constraint values
 * @input: n: Length of the xopt
 * @input: x: initial guess values
 * @input: grad: Target pointer for the gradient vector
 * @input: f_data: Formulation parameter
 * @output: objective value
 **/
double objective_fn(unsigned n, const double *x, double *grad, void *f_data) {

    struct problem_data *problem_data = static_cast<struct problem_data *>(f_data);
    struct scenario_parameter *scenario = problem_data->scenario;
    struct problem_parameter *prob_param = problem_data->prob_param;

    if (grad) {
        /* OBJECTIVE_JACOBIAN PLACEHOLDER*/
    }

    double obj_value;
    /* OBJECTIVE PLACEHOLDER*/
    return obj_value;
}

/** @input m: Amount of constraints
 * @input: result: Target vector for the constraint values
 * @input: n: Length of the xopt
 * @input: x: initial guess values
 * @input: grad: Target pointer for the gradient matrix
 * @input: f_data: Formulation parameter
 **/
void constraint_fn(unsigned m, double *result, unsigned n, const double *x, double *grad, void *f_data) {
    struct problem_data *problem_data = static_cast<struct problem_data *>(f_data);
    struct scenario_parameter *scenario = problem_data->scenario;
    struct problem_parameter *prob_param = problem_data->prob_param;

    /** f(x) <= 0 */
    /* CONSTRAINTS PLACEHOLDER*/

    if (grad) {
        /* CONSTRAINTS_JACOBIAN PLACEHOLDER*/
    }
}


void initial_guess_fn(double *result, unsigned n, const double *x, void *f_data) {
    struct problem_data *problem_data = static_cast<struct problem_data *>(f_data);
    struct scenario_parameter *scenario = problem_data->scenario;
    struct problem_parameter *prob_param = problem_data->prob_param;

    /* INITIAL_GUESS PLACEHOLDER*/
}

void lower_bound_fn(double *result, unsigned n, const double *x, void *f_data) {
    struct problem_data *problem_data = static_cast<struct problem_data *>(f_data);
    struct scenario_parameter *scenario = problem_data->scenario;
    struct problem_parameter *prob_param = problem_data->prob_param;

    /* LBX PLACEHOLDER*/
}

void upper_bound_fn(double *result, unsigned n, const double *x, void *f_data) {
    struct problem_data *problem_data = static_cast<struct problem_data *>(f_data);
    struct scenario_parameter *scenario = problem_data->scenario;
    struct problem_parameter *prob_param = problem_data->prob_param;


    /* UBX PLACEHOLDER*/
}

void optimized_variable_fn(optimized_variable *xopt, unsigned n, const double *x) {

    /* OPTIMIZED_VARIABLE PLACEHOLDER*/

}

double sq(double var_in) {
    return pow(var_in, 2);
}

/* OS STREAM PLACEHOLDER*/

std::ostream &operator<<(std::ostream &os, const optimizer_info &o) {
    return os << "{ status: " << o.status << ", costs: " << o.costs << ", active_box_limits: " << o.active_box_limits.transpose() << ", active_constraints: " << o.active_constraints.transpose()
           << ", violated_active_box_limits: " << o.violated_box_limits.transpose() << ", violated_constraints: " << o.violated_constraints.transpose() << " }";
};
