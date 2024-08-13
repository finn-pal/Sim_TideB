import time

import matplotlib.pyplot as plt
import pynbody

from src import make_plots

start = time.time()

# particle select
IORD = 3
PARTCLE_TYPE = "stars"

# data loop details
INIT_TIME = 1  # initial file
TIMESTEP = 1  # time step between snapshots (Myr)
NUM_TIMESTEP = 5  # number of time steps

# get_particle(
#     PARTCLE_TYPE,
#     IORD,
#     INIT_TIME,
#     NUM_TIMESTEP,
# )

# data folder location
DATA_FLDRPTH = "/Users/z5114326/Desktop/Tets/"
BASE_FILE = "GLX.000001"

s = pynbody.load(DATA_FLDRPTH + BASE_FILE)
s.physical_units()

make_plots.plt_stellar_density(s, plt_show=False)

end = time.time()
print("Runtime " + str(round(end - start, 2)) + " seconds")
