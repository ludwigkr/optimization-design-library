#pragma once
#include "sqpmethod.h"
#ifdef USE_OSQP
#include "min_nlp_quad_opti_osqp.h"
#else
#include "min_nlp_quad_opti_qpoases.h"
#endif

class MinNLPInterface {
public:
    bool use_casadi = false;
    void init();
    Eigen::VectorXd find_optimal_solution(Eigen::VectorXd scenario);

private:
    SQPSolver sqpsolver;
    MinNlpQuadraticOptimizer qpsolver;

};
