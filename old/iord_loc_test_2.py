import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pynbody
import pynbody.plot.sph as sph

# data folder location
DATA_FLDRPTH = "/Users/z5114326/Desktop/Tets/"
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
    s.stars, qty="rho", width="100 kpc", cmap="Blues", units="g cm^-2", show_cbar=True, subplot=axG
)  # proj
plt.xlabel("$x \\;{\\rm [kpc]}$", fontsize=15)
plt.ylabel("$y \\;{\\rm [kpc]}$", fontsize=15)
axG.annotate(timestr + "Myr", xy=(0.7, 0.9), xycoords="axes fraction", color="white", fontsize=13)

y = s.s["iord"]
x_pos = [pos[0] for pos in s.s["pos"]]
y_pos = [pos[1] for pos in s.s["pos"]]


y1 = [yi for yi in y if yi > 10084106]
x1_pos = [xi_pos for xi_pos, yi in zip(x_pos, y) if yi > 10084106]
y1_pos = [yi_pos for yi_pos, yi in zip(y_pos, y) if yi > 10084106]

x1_pos = [
    xi_pos
    for xi_pos, yi_pos in zip(x_pos, y_pos)
    if yi_pos >= 29 and yi_pos <= 36 and xi_pos >= -4 and xi_pos <= 3
]
y1_pos = [
    yi_pos
    for xi_pos, yi_pos in zip(x_pos, y_pos)
    if yi_pos >= 29 and yi_pos <= 36 and xi_pos >= -4 and xi_pos <= 3
]

iord_cont = [
    iord
    for iord, xi_pos, yi_pos in zip(y, x_pos, y_pos)
    if yi_pos >= 29 and yi_pos <= 36 and xi_pos >= -4 and xi_pos <= 3
]

print(min(iord_cont), max(iord_cont), len(iord_cont))

plt.scatter(x1_pos, y1_pos, c="magenta", s=2)
# plt.show()

plt.savefig("part_select/figs_ps/stellar_density2")
