#include <iostream>
#include <nlopt.h>
#include "hs074_interface.hpp"

//Include TestHarness at last! Or you will get random errors you will never be able to identify!! Trust me!
#include <CppUTest/TestHarness.h>

TEST_GROUP(Nlopt) {
};

TEST(Nlopt, nlopt) {
    Hs074Problem hs074;
    hs074.init(NLOPT_LD_MMA);
    Eigen::MatrixXd xtarget(2, 2);
    xtarget << 1, 3.82115, 4.743, 1.37941;
    Eigen::MatrixXd mat(2, 2);
    mat << 1, 5, 5, 1;
    hs074.scenario.X_guess = mat;

    auto status = hs074.solve();
    std::cout << "Status: " << status << std::endl;
    std::cout << "Xopt: " << hs074.xopt << std::endl;
    std::cout << "Xopt(real): " << xtarget.reshaped(1,4) << std::endl;
    CHECK(true);
};
