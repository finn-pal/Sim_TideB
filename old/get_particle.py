from enum import Enum

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pynbody


class ParticleType(Enum):
    stars = "stars"
    gas = "gas"
    dm = "dm"
    all_types = ""


def get_particle(
    p_type: ParticleType, iord: int, init_time: int = 1, timestep: int = 1, num_timestep: int = 0
):
    # type assertion
    if p_type not in ParticleType:
        raise ValueError("%r is not valid; possible choices: %r" % (p_type, list(ParticleType)))

    # data folder location
    # DATA_FLDRPTH = "/Volumes/My Passport for Mac/TideB/"
    DATA_FLDRPTH = "/Users/z5114326/Desktop/Tets/"

    # file naming
    BASE_FILE = "GLX.000000"
    init_file = BASE_FILE[: -len(str(init_time))] + str(init_time)
    init_file_num = init_file.split(".")[-1]
    next_time_num = init_file_num

    i = 0
    while i <= num_timestep:
        next_file = init_file[: -len(next_time_num)] + next_time_num
        filepath = DATA_FLDRPTH + next_file

        # do code looping here
        s = pynbody.load(filepath)
        s.physical_units()
        # t_now = s.properties["time"].in_units("Myr")
        # timestr = str(np.round(float(t_now), 1))

        i_ord_pos = s[iord]["pos"][0]
        print(i_ord_pos)

        # next loop step
        past_file_num = next_time_num
        next_time_num = str(int(past_file_num) + timestep)
        i = i + 1
