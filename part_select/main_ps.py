import time

from func_ps.get_particle import get_particle

start = time.time()

# particle select
IORD = 3
PARTCLE_TYPE = "stars"

# data loop details
INIT_TIME = 1  # initial file
TIMESTEP = 1  # time step between snapshots (Myr)
NUM_TIMESTEP = 5  # number of time steps

get_particle(
    PARTCLE_TYPE,
    IORD,
    INIT_TIME,
    NUM_TIMESTEP,
)

end = time.time()
print("Runtime " + str(round(end - start, 2)) + " seconds")
