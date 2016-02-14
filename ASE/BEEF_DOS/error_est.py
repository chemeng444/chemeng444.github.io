from ase.dft.bee import BEEF_Ensemble

import numpy as np
import os

ens = BEEF_Ensemble()

# read out the energy and the absolute error for that energy
energy, error = ens.read('file.bee')

# subtract energies and errors to get the respective
# adsorption energies and errors on the adsorption energies
