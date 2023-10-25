import numpy as np
def calculate_n_units(x_train, n_basis_functions, units_multiplier):
    num_unique_vals = [len(np.unique(x_train[:, i])) for i in range(x_train.shape[1])]
    return [min(n_basis_functions, i * units_multiplier) for i in num_unique_vals]
