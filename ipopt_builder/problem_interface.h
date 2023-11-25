#pragma once
#define HAVE_STDDEF_H
#include <IpIpoptApplication.hpp>
#include <IpSolveStatistics.hpp>
#include "problem_formulation_ipopt.h"
#undef HAVE_CSTDDEF_H

using namespace Ipopt;

class Problem_Interface {

public:
    scenario_parameter scenario;
    problem_parameter prob_param;
    optimized_variable xopt;
    Problem_Interface();
    int solve();

private:
    SmartPtr<TNLP> mynlp;
    SmartPtr<IpoptApplication> app;
    ApplicationReturnStatus status;

};
