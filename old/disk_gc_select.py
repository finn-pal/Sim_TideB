import time

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pynbody
import pynbody.plot.sph as sph

start = time.time()

# data folder location
# DATA_FLDRPTH = "/Users/z5114326/Desktop/Tets/"
DATA_FLDRPTH = "/Volumes/My Passport for Mac/TideB/"

params = {"font.family": "serif", "mathtext.fontset": "stix", "font.size": 12}
matplotlib.rcParams.update(params)

# data loop details
INIT_TIME = 330
TIMESTEP = 10
NUM_TIMESTEP = 0

BASE_FILE_0 = "GLX.000000"
BASE_FILE_1 = "GLX.00000"

INIT_FILE_0 = BASE_FILE_0[: -len(str(INIT_TIME))] + str(INIT_TIME)
INIT_FILE_1 = BASE_FILE_1[: -len(str(INIT_TIME))] + str(INIT_TIME)

i = 0

if int(INIT_TIME) < 610:
    init_file_num = INIT_FILE_0.split(".")[-1]
else:
    init_file_num = INIT_FILE_1.split(".")[-1]

next_time_num = init_file_num

if int(next_time_num) < 610:
    next_file = INIT_FILE_0[: -len(next_time_num)] + next_time_num

else:
    next_file = INIT_FILE_1[: -len(next_time_num)] + next_time_num

filepath = DATA_FLDRPTH + next_file

# do code looping here
s = pynbody.load(filepath)
s.physical_units()
t_now = s.properties["time"].in_units("Myr")
timestr = str(int(np.round(float(t_now), 1)))

part_ls = []

com_id_min = 1008463671
com_id_max = 1008473670

s_com = s.s[(s.s["iord"] >= com_id_min) & (s.s["iord"] <= com_id_max)]

focus_id = [iord for iord, yi in zip(s_com["iord"], s_com["y"]) if yi > -10]

print(focus_id)
