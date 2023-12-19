#pragma once
#define HAVE_STDDEF_H
#include <IpIpoptApplication.hpp>
#include <IpSolveStatistics.hpp>
#undef HAVE_CSTDDEF_H

using namespace Ipopt;

void set_all_default_settings(SmartPtr<IpoptApplication> *app);
