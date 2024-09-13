#pragma once
#include <math.h>
#include <eigen3/Eigen/Core>


struct scenario_parameter;
struct problem_parameter;
struct optimized_variable;

struct problem_data {
    struct scenario_parameter scenario;
    struct problem_parameter prob_param;

    problem_data() {
        scenario = scenario_parameter();
        prob_param = problem_parameter();
    }
};

double objective_fn(unsigned n, const double *x, double *grad, void *f_data);
void constraint_fn(unsigned m, double *result, unsigned n, const double *x, double *grad, void *f_data);
void initial_guess_fn(double *result, unsigned n, const double *x, void *f_data);
void lower_bound_fn(double *result, unsigned n, const double *x, void *f_data);
void upper_bound_fn(double *result, unsigned n, const double *x, void *f_data);
void optimized_variable_fn(optimized_variable *xopt, unsigned n, const double *x);
double sq(double var_in);

std::ostream &operator<<(std::ostream &os, const scenario_parameter &s);
std::ostream &operator<<(std::ostream &os, const problem_parameter &p);
std::ostream &operator<<(std::ostream &os, const optimized_variable &o);
