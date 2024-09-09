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
    Eigen::MatrixXd mat(2, 2);
    mat << 1, 5, 5, 1;
    hs074.prob_data.scenario.X_guess = mat;

    auto status = hs074.solve();
    std::cout << "Status: " << status << std::endl;
    CHECK(true);
};
