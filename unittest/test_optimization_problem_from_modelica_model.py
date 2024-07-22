import numpy as np
import math
import unittest
import casadi
import sys

sys.path.append("..")
sys.path.append("../openmodelica_parser")

from variables import Variables
from optimization_problem_from_modelica_model import optimization_problem_from_modelica_model
import optimizationconfiguration as optconfig
import optimizationsolver

class TestOptimizationProblemFromModelicaModel(unittest.TestCase):
    def setUp(self) -> None:
        return super().setUp()

    def test_create_op_from_om_model(self):
        file_path = "./testdata/simple_oscillator.txt"
        model_inputs = ['force2.f']
        dt = 0.1
        K = 10

        op = optimization_problem_from_modelica_model(file_path, model_inputs, dt=dt, K=K)
        self.assertTrue(op.constraints.n_constraints == 2*(K-1) + (K-1))
        self.assertTrue(op.optvars.n_vars == 3*K + 1*(K-1))
        self.assertTrue(op.problem_parameters.n_vars == 3)

        op.problem_parameters.register('s_ref', K)

        scenario = Variables()
        scenario.register("s0")
        scenario.register("v0")
        scenario.register("a0")
        op.scenario_parameters = scenario

        init_guess = casadi.SX(op.optvars.n_vars, 1)
        init_guess[op.optvars.idxs['mass2_s']] = scenario.variables_by_names('s0')
        init_guess[op.optvars.idxs['mass2_v']] = scenario.variables_by_names('v0')
        init_guess[op.optvars.idxs['mass2_a']] = scenario.variables_by_names('a0')
        init_guess[op.optvars.idxs['force2_f']] = 1
        op.register_initial_guess_function(init_guess)

        lbx = casadi.SX(op.optvars.n_vars, 1)
        lbx[op.optvars.idxs['mass2_s']] = -math.inf
        lbx[op.optvars.idxs['mass2_s'][0,0]] = scenario.variables_by_names('s0')
        lbx[op.optvars.idxs['mass2_v']] = -math.inf
        lbx[op.optvars.idxs['mass2_v'][0,0]] = scenario.variables_by_names('v0')
        lbx[op.optvars.idxs['mass2_a']] = -math.inf
        lbx[op.optvars.idxs['mass2_a'][0,0]] = scenario.variables_by_names('a0')
        lbx[op.optvars.idxs['force2_f']] = -100
        print(f"{lbx = }")
        op.register_lower_box_limits_function(lbx)

        ubx = casadi.SX(op.optvars.n_vars, 1)
        ubx[op.optvars.idxs['mass2_s']] = math.inf
        ubx[op.optvars.idxs['mass2_s'][0,0]] = scenario.variables_by_names('s0')
        ubx[op.optvars.idxs['mass2_v']] = math.inf
        ubx[op.optvars.idxs['mass2_v'][0,0]] = scenario.variables_by_names('v0')
        ubx[op.optvars.idxs['mass2_a']] = math.inf
        ubx[op.optvars.idxs['mass2_a'][0,0]] = scenario.variables_by_names('a0')
        ubx[op.optvars.idxs['force2_f']] = 100
        op.register_upper_box_limits_function(ubx)

        lbg = casadi.SX(op.constraints.n_constraints, 1)
        lbg[:] = 0
        op.register_lower_inequality_constraint_limits_function(lbg)

        ubg = casadi.SX(op.constraints.n_constraints, 1)
        ubg[:] = 0
        op.register_upper_inequality_constraint_limits_function(ubg)

        objective = casadi.sum1((op.optvars.variables_by_names('mass2_s') - op.problem_parameters.variables_by_names('s_ref'))**2)
        op.register_objective(objective)


        pos0 = 10
        vel0 = 5
        acc0 = 0
        scenario0 = op.scenario_parameters.unpacked([pos0, vel0, acc0])
        print(f"{op.problem_parameters.idxs}")

        mass = 1
        spring_c = 0.5
        damper_d = 0.1
        s_ref = np.zeros([1,K])
        prob_param0 = op.problem_parameters.unpacked([mass, spring_c, damper_d, s_ref])
        
        opts = optconfig.load_optimizer_settings("ipopt")
        solver = optimizationsolver.build_solver(op, opts)


        result = optimizationsolver.run(solver, op, scenario0, prob_param0)

        disp_txt = optimizationsolver.formulation(op, scenario0, prob_param0, result)
        with open('op-simple-oscilator.org', 'w') as f:
            f.write(disp_txt)

        print(op.optvars.idxs.keys())
        print(op.optvars.packed(result['x']))
        pass

if __name__ == "__main__":
    unittest.main()
