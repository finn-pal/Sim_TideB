import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pynbody
import pynbody.plot.sph as sph

# data folder location
# DATA_FLDRPTH = "/Volumes/My Passport for Mac/TideB/"
DATA_FLDRPTH = "/Users/z5114326/Desktop/Tets/"
# file naming
BASE_FILE = "GLX.000010"

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
# plt.show()

# pos_test_l = [1 if s_pos[1] > 20 else 0 for s_pos in s.s["pos"]]
# pos_test = [s_iord if s_pos[1] > 20 else 0 for s_iord, s_pos in zip(s.s["iord"], s.s["pos"])]
# comp_ls = [pos_iord for pos_iord in pos_test if pos_iord != 0]


# x = [s.s[s.s["iord"] == iord]["pos"][0][0] for iord in comp_ls]
# y = [s.s[s.s["iord"] == iord]["pos"][0][1] for iord in comp_ls]

# plt.scatter(x[-1], y[-1], s=20, c="magenta")

# plt.savefig("part_select/figs_ps/stellar_density")

# plt.figure(2)
# plt.scatter(comp_ls, [0] * len(comp_ls))

i = 0
x1 = []
y1 = []

for iord in s["iord"]:
    x1.append(i)
    y1.append(iord)
    i += 1

y_jump = [y11 for y11 in y1 if y11 > 1e9]
i_ord_test = y_jump[int(len(y_jump) / 2)]

print(i_ord_test)
print("gas ", s.g[s.g["iord"] == i_ord_test]["iord"])
print("stars ", s.s[s.s["iord"] == i_ord_test]["iord"])
print("dm ", s.dm[s.dm["iord"] == i_ord_test]["iord"])

x3 = s[s["iord"] == i_ord_test]["pos"][0][0]
y3 = s[s["iord"] == i_ord_test]["pos"][0][0]

plt.scatter(x3, y3, s=20, c="magenta")

plt.savefig("part_select/figs_ps/stellar_density")

# plt.scatter(x1, y1)
# plt.show()

# print("gas ", len(s.g))
# print("stars ", len(s.s))
# print("dm ", len(s.dm))
# print("total ", len(s), len(s.g) + len(s.s) + len(s.dm))
# print()

# print(s["iord"][-1])
# print(s[s["iord"] == s["iord"][-1]]["iord"][0])
# print(s["iord"].index(s["iord"][-1]))

# print(len(comp_ls))
# print(comp_ls[-1], comp_ls[0])

# print(s.s["iord"])
# print(s.s["pos"][0][1])
