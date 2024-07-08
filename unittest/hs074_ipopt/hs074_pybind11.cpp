#include <pybind11/pybind11.h>
#include "hs074_interface.h"

namespace py = pybind11;

PYBIND11_MODULE(pyhs074, m) {
    py::class_<Hs074_Interface>(m, "Hs074_Interface")
    .def(py::init<>());
}
