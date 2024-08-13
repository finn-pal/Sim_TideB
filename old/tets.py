import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pynbody
import pynbody.plot.sph as sph
from matplotlib.animation import PillowWriter

# data folder location
DATA_FLDRPTH = "/Users/z5114326/Desktop/Tets/"
# DATA_FLDRPTH = "/Volumes/My Passport for Mac/TideB/"

# data loop details
INIT_TIME = 1

BASE_FILE = "GLX.000000"
INIT_FILE = BASE_FILE[: -len(str(INIT_TIME))] + str(INIT_TIME)
filepath = DATA_FLDRPTH + INIT_FILE

print(INIT_FILE)

s = pynbody.load(filepath)
s.physical_units()
t_now = s.properties["time"].in_units("Myr")
timestr = str(np.round(float(t_now), 1))

id = s.s["iord"]
# eps = s.s["eps"]
# y = [0] * len(id)

# y1 = []

# i = 0
# for i in range(0, len(id)):
#     y1.append(i)
#     i += 1


# plt.scatter(y1, id)
# plt.yscale("log")
# plt.show()

iod = pd.DataFrame(data=s["iord"])
comp = iod[(iod["iord"] >= 1008463671) & (iod["iord"] <= 1008473670)]

plt.hist(s.s["mass"])

# plt.figure()
# plt.scatter(iod.index, iod["iord"])
# plt.scatter(comp.index, comp["iord"], c="r")
# plt.ylim([0, 1e6])

# plt.figure()
# plt.scatter(iod.index, iod["iord"])
# plt.scatter(comp.index, comp["iord"], c="r")
# plt.ylim([1e9, 1009034882 + 1000])
# plt.yscale1("log")
# plt.hist(iod["iord"])
# plt.scatter(id, y)
# plt.hist(id)
plt.show()
