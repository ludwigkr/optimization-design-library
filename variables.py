#!/usr/bin/env python3
import casadi
import numpy as np

class Variables:
    def __init__(self):
        self.n_vars = 0
        self.idxs = {} # saves idxs of blocks: name: [0, 1, 2,..]
        self.variables = [] # list of variables in blocks
        self.names = []

    def __update_index(self, new_vars):
        """Based on the new opimization variables optvars, determines their indices optvars_idxs and returns the updated total amount of optimizatin variables (which is seen for further optimization variables as prev_variable index) prev_n."""
        optvars_idxs = np.linspace(0, new_vars.size1() * new_vars.size2() - 1, new_vars.size1() * new_vars.size2(), dtype=int) + self.n_vars
        self.n_vars += new_vars.size1() * new_vars.size2()

        return optvars_idxs.reshape((new_vars.size1(), new_vars.size2()), order='F')

    def register(self, name, new_vars):
        assert(type(new_vars) == casadi.casadi.SX)
        assert(type(name) == str)
        self.idxs[name] = self.__update_index(new_vars)
        self.variables.append(new_vars)
        self.names.append(name)

    def block_by_name(self, name):
        assert(name in self.names)
        return self.variables[self.idxs[name][0, 0]]

    def variables_flat(self):
        """Function to get the symbolic vector in mathematical form."""
        if self.n_vars > 0:
            return casadi.vertcat(*[casadi.reshape(e, -1, 1) for e in self.variables])
        else:
            return []

    def unpacked(self, variables=None):
        if variables is None:
            return self.variables_flat()
        else:
            if type(variables) != list and type(variables) != np.ndarray:
                return np.array([float(variables)])
            else:
                if type(variables[0]) != list and type(variables[0]) != np.ndarray:
                    return np.array(variables).reshape(-1, 1)
                else:
                    ret = np.array(variables[0]).reshape(-1, 1)
                    for var_block in variables[1:]:
                        ret = np.vstack((ret, np.array(var_block).reshape(-1, 1)))
                    return ret

    def packed(self, variables=None):
        if variables is None:
            return self.variables
        else:
            fn = casadi.Function('fn', [self.variables_flat()], self.variables, ['flat'], self.names)
            return fn(variables)


    def unpack_variables_fn(self):
        """Function to convert structured variables to flat variables."""
        # casadi.Function('function_name', [inputs], [outputs], ['input_names'], ['output_names])
        return casadi.Function('pack_variables_fn', self.variables, [self.variables_flat()], self.names, ['flat'])

    def pack_variables_fn(self):
        """Function to convert convert flat variables to structured variables."""
        return casadi.Function('unpack_variables_fn', [self.variables_flat()], self.variables, ['flat'], self.names)
