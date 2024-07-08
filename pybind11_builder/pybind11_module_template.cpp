
#include <pybind11/pybind11.h>
#include <pybind11/eigen.h>
#include "optproblem_interface.h"

namespace py = pybind11;

PYBIND11_MODULE(optproblem, m) {
    py::class_<Optproblem_Interface>(m, "Optproblem_Interface")
    .def(py::init<>())
    .def_readwrite("scenario", &Optproblem_Interface::scenario)
    .def_readwrite("xopt", &Optproblem_Interface::xopt)
    .def_readwrite("prob_param", &Optproblem_Interface::prob_param)
    .def("solve", &Optproblem_Interface::solve);

    py::class_<scenario_parameter>(m, "scenario_parameter")
    /** SCENARIO PARAMETER INITIALIZATIONS */
    /** SCENARIO PARAMETER ELEMENTS */
    .def("norm", &scenario_parameter::norm);

    py::class_<problem_parameter>(m, "problem_parameter")
    /** PROBLEM PARAMETER INITIALIZATIONS */
    /** PROBLEM PARAMETER ELEMENTS */
    .def("norm", &problem_parameter::norm);

    py::class_<optimized_variable>(m, "optimized_variable")
    /** OPTIMIZED VARIABLE INITIALIZATIONS */
    /** OPTIMIZED VARIABLE ELEMENTS */
    .def("norm", &optimized_variable::norm);
}
