import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pynbody
import pynbody.plot.sph as sph

# data folder location
DATA_FLDRPTH = "/Users/z5114326/Desktop/Tets/"
# DATA_FLDRPTH = "/Volumes/My Passport for Mac/TideB/"

BASE_FILE = "GLX.000001"

params = {"font.family": "serif", "mathtext.fontset": "stix"}
matplotlib.rcParams.update(params)

filepath = DATA_FLDRPTH + BASE_FILE
s = pynbody.load(filepath)
s.physical_units()

t_now = s.properties["time"].in_units("Myr")
timestr = str(np.round(float(t_now), 1))

post = s.stars
s_iord_ls = post["iord"]
s_eps = post["eps"]

x_pos = [pos[0] for pos in post["pos"]]
y_pos = [pos[1] for pos in post["pos"]]

# eps_val = 0.01
# eps_val = 0.05
# eps_val = 0.10
eps_val = 0.20  # companion

eps_val_comp = 0.20

# x = [x for x, eps in zip(x_pos, s_eps) if round(eps, 2) == eps_val]
# y = [x for x, eps in zip(y_pos, s_eps) if round(eps, 2) == eps_val]

y = [0] * len(s_iord_ls)

comp_iords = [iord for iord, eps_i in zip(s_iord_ls, s_eps) if round(eps_i, 2) == eps_val_comp]

print(min(comp_iords), max(comp_iords), max(comp_iords) - min(comp_iords) + 1, len(comp_iords))

all_iord = s_iord_ls.copy()

zero_ls = []
for i in range(0, len(all_iord)):
    zero_ls.append(0)

plt.figure(1)
plt.scatter(all_iord, zero_ls, s=5)
plt.axvspan(min(comp_iords), max(comp_iords), color="crimson", alpha=0.1)
plt.savefig("part_select/figs_ps/comp_test")

i_iord_weird = [i for i, eps_i in zip(s_iord_ls, s_eps) if round(eps_i, 2) == 0.01]
x_weird = [x_i for x_i, eps_i in zip(x_pos, s_eps) if round(eps_i, 2) == 0.01]
y_weird = [y_i for y_i, eps_i in zip(y_pos, s_eps) if round(eps_i, 2) == 0.01]

print(min(i_iord_weird))

vmin = 3e-4
vmax = 8e-2
plt.clf()
figG = plt.figure(2)
axG = figG.add_subplot(1, 1, 1)
imG = sph.image(
    s.s, qty="rho", width="200 kpc", cmap="Blues", units="g cm^-2", show_cbar=True, subplot=axG
)  # proj
plt.xlabel("$x \\;{\\rm [kpc]}$", fontsize=15)
plt.ylabel("$y \\;{\\rm [kpc]}$", fontsize=15)
axG.annotate(timestr + "Myr", xy=(0.7, 0.9), xycoords="axes fraction", color="white", fontsize=13)

plt.scatter(x_weird, y_weird, c="magenta", s=2)
plt.savefig("part_select/figs_ps/muck")
