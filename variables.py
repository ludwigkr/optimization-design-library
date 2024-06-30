#!/usr/bin/env python3
import casadi
from casadi import SX, DM
import numpy as np
import itertools

class Variables:
    def __init__(self):
        self.n_vars = 0
        self.idxs = {} # saves idxs of blocks: name: [0, 1, 2,..]
        self.variables = [] # list of variables in blocks
        self.names = []

    def __str__(self) -> str:
        ret = ""
        for n, name in enumerate(self.names):
            ret += f"{name}{self.variables[n].size()}: {np.array(self.idxs[name]).reshape(-1).tolist()}\n"
        return ret

    def register(self, name:str, dim=None):
        if type(dim) == int:
            new_vars = casadi.SX.sym(name, dim)
        elif type(dim) == list:
            new_vars = casadi.SX.sym(name, dim[0], dim[1])
        elif dim is None:
            new_vars = casadi.SX.sym(name)
        else:
            raise RuntimeError("Wrong dimensionn type.")
        assert(type(new_vars) == casadi.casadi.SX)
        assert(type(name) == str)
        self.idxs[name] = self.__update_index(new_vars)
        self.variables.append(new_vars)
        self.names.append(name)
        return new_vars

    def __update_index(self, new_vars: casadi.SX):
        """Based on the new opimization variables optvars, determines their indices optvars_idxs and returns the updated total amount of optimizatin variables (which is seen for further optimization variables as prev_variable index) prev_n."""
        optvars_idxs = np.linspace(0, new_vars.size1() * new_vars.size2() - 1, new_vars.size1() * new_vars.size2(), dtype=int) + self.n_vars
        self.n_vars += new_vars.size1() * new_vars.size2()

        return optvars_idxs.reshape((new_vars.size1(), new_vars.size2()), order='F')

    def remove(self, name:str):
        if name in self.idxs:
            del self.idxs[name]
            i = [i for i in range(len(self.names)) if self.names[i] == name][0]
            del self.variables[i]
            del self.names[i]
        
        self.__reindex()

    def __reindex(self):
        self.n_vars = 0
        for n in range(len(self.names)):
            name = self.names[n]
            self.idxs[name] = self.__update_index(self.variables[n])


    def variables_by_names(self, names):
        if type(names) == str:
            assert(names in self.names)
            idx = self.idxs[names]
        else:
            idx = []
            for n in names:
                assert(n in self.names)
                idx.append(self.idxs[n].tolist())
            idx = np.array(idx).reshape([-1]).tolist()
        return self.variables_flat()[idx]


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
                if len(variables) == 0 and type(variables[0]) != list and type(variables[0]) != np.ndarray:
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

if __name__ == "__main__":
    import unittest



    unittest.main()
