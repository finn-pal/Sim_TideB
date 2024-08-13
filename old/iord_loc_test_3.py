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

# -- Face-on gas density plot
print("plotting stars")
vmin = 3e-4
vmax = 8e-2
plt.clf()
figG = plt.figure(1)
axG = figG.add_subplot(1, 1, 1)
imG = sph.image(
    s.s, qty="rho", width="200 kpc", cmap="Blues", units="g cm^-2", show_cbar=True, subplot=axG
)  # proj
plt.xlabel("$x \\;{\\rm [kpc]}$", fontsize=15)
plt.ylabel("$y \\;{\\rm [kpc]}$", fontsize=15)
axG.annotate(timestr + "Myr", xy=(0.7, 0.9), xycoords="axes fraction", color="white", fontsize=13)

post = s.stars

s_iord_ls = post["iord"]
s_eps = post["eps"]

x_pos = [pos[0] for pos in post["pos"]]
y_pos = [pos[1] for pos in post["pos"]]

# eps_val = 0.01
# eps_val = 0.05
# eps_val = 0.10
eps_val = 0.20  # companion

x = [x for x, eps in zip(x_pos, s_eps) if round(eps, 2) == eps_val]
y = [x for x, eps in zip(y_pos, s_eps) if round(eps, 2) == eps_val]

print(len(x), len(y))

plt.scatter(x, y, c="magenta", s=2)
plt.savefig("part_select/figs_ps/test")

plt.figure(2)
plt.scatter(s_iord_ls, s_eps, c="blue", s=2)
plt.xlabel("iord")
plt.ylabel("eps")
plt.savefig("part_select/figs_ps/stellar_eps")
