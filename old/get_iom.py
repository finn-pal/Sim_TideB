# %%

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
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

com_id_min = 1008463671
com_id_max = 1008473670

# com_x = [ps[0] for ps, id in zip(star["pos"], star["iord"]) if id >= com_id_min and id <= com_id_max]
# s_cen_r = [
#     rad for rad, id in zip(s.s["r"].in_units("kpc"), s.s["iord"]) if not id >= com_id_min and id <= com_id_max
# ]

# kpc
rx = [r[0] for r, id in zip(s.s["pos"], s.s["iord"]) if not id >= com_id_min and id <= com_id_max]
ry = [r[1] for r, id in zip(s.s["pos"], s.s["iord"]) if not id >= com_id_min and id <= com_id_max]
rz = [r[2] for r, id in zip(s.s["pos"], s.s["iord"]) if not id >= com_id_min and id <= com_id_max]

# km / s
vx = [v[0] for v, id in zip(s.s["vel"], s.s["iord"]) if not id >= com_id_min and id <= com_id_max]
vy = [v[1] for v, id in zip(s.s["vel"], s.s["iord"]) if not id >= com_id_min and id <= com_id_max]
vz = [v[2] for v, id in zip(s.s["vel"], s.s["iord"]) if not id >= com_id_min and id <= com_id_max]

# km **2 / s ** 2
e_pot = [phi for phi, id in zip(s.s["phi"], s.s["iord"]) if not id >= com_id_min and id <= com_id_max]
e_kin = [0.5 * (vxi**2 + vyi**2 + vzi**2) for vxi, vyi, vzi in zip(vx, vy, vz)]
e_tot = [e_kini + e_poti for e_kini, e_poti in zip(e_kin, e_pot)]

# kpc km / s
l_z = [rxi * vyi - ryi * vxi for rxi, ryi, vxi, vyi in zip(rx, ry, vx, vy)]

plt.scatter(np.array(l_z) * 10**-3, np.array(e_tot) * 10**-5)
plt.xlabel("$L_{z}$ ($10^{3}$ $kpc$ $km$ $s^{-1}$)")
plt.ylabel("E ($10^{5}$ $km^{2}$ $s^{-2}$)")
plt.show()

plt.figure()
plt.plot(s.s["r"].in_units("kpc"), np.array(s.s["phi"]) * 10**-5, "k.")
plt.xlabel("r (kpc)")
plt.ylabel("E_potential ($10^{5}$ $km^{2}$ $s^{-2}$)")
plt.show()

# min_v = 2
# max_v = 5

# lst = np.linspace(0, 10, 11)

# lst_rev = [ls for ls in lst if ls <= min_v and ls >= ]

# %%
