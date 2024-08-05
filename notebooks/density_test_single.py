import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pynbody
import pynbody.plot.sph as sph
from mpl_toolkits.axes_grid1 import make_axes_locatable

# data folder location
# DATA_FLDRPTH = "/Users/z5114326/Desktop/Tets/"
DATA_FLDRPTH = "/Volumes/My Passport for Mac/TideB/"

# data loop details
INIT_TIME = 1

# BASE_FILE = "GLX.00000"
BASE_FILE = "GLX.000000"
INIT_FILE = BASE_FILE[: -len(str(INIT_TIME))] + str(INIT_TIME)
filepath = DATA_FLDRPTH + INIT_FILE

print(INIT_FILE)

s = pynbody.load(filepath)
s.physical_units()
t_now = s.properties["time"].in_units("Myr")
timestr = str(int(np.round(float(t_now), 1)))

vmin = 1e-2
vmax = 1e5
cmap = "bone"

params = {"font.family": "serif", "mathtext.fontset": "stix", "font.size": 12}
matplotlib.rcParams.update(params)

fig, axs = plt.subplots(nrows=2, ncols=2, figsize=(10, 10))

ax0 = axs[0, 0]
ax1 = axs[0, 1]
ax2 = axs[1, 0]
ax3 = axs[1, 1]

im = sph.image(
    s.s,
    qty="rho",
    width="200 kpc",
    cmap=cmap,
    units="Msol pc^-2",
    show_cbar=False,
    log=True,
    vmin=vmin,
    vmax=vmax,
    resolution=500,
    subplot=ax0,
)

divider = make_axes_locatable(ax0)
cax = divider.append_axes("top", size="5%", pad=0.10)
im_c = ax0.imshow(np.array([[np.log10(vmin), np.log10(vmax)]]), cmap=cmap, origin="lower")
im_c.set_visible(False)
fig.colorbar(im_c, cax=cax, orientation="horizontal")
cax.xaxis.tick_top()
cax.xaxis.set_label_position("top")
cax.set_xticks([-2, -1, 0, 1, 2, 3, 4, 5])
cax.set_xlabel("log$_{10}$ Stellar Density [M$_\u2609$ pc$^{-2}$]", labelpad=10)

ticks = np.linspace(-100, 100, 5)
ax0.set_facecolor("black")
ax0.annotate(timestr + " Myr", xy=(0.7, 0.9), xycoords="axes fraction", color="white", fontsize=13)
ax0.set_xlabel("$x \\;{\\rm [kpc]}$", fontsize=13)
ax0.set_ylabel("$y \\;{\\rm [kpc]}$", fontsize=13, labelpad=-10)
ax0.set(xticks=ticks, yticks=ticks)

com_id_min = 1008463671
com_id_max = 1008473670

s_cen = s.s[(s.s["iord"] < com_id_min) | (s.s["iord"] > com_id_max)]

s_com = s.s[(s.s["iord"] >= com_id_min) & (s.s["iord"] <= com_id_max)]

# kpc
x_cen = [xi for xi in s_cen["x"]]
y_cen = [yi for yi in s_cen["y"]]
z_cen = [zi for zi in s_cen["z"]]

x_com = [xi for xi in s_com["x"]]
y_com = [yi for yi in s_com["y"]]
z_com = [zi for zi in s_com["z"]]

# km / s
vx_cen = [vxi for vxi in s_cen["vx"]]
vy_cen = [vyi for vyi in s_cen["vy"]]
vz_cen = [vzi for vzi in s_cen["vz"]]

vx_com = [vxi for vxi in s_com["vx"]]
vy_com = [vyi for vyi in s_com["vy"]]
vz_com = [vzi for vzi in s_com["vz"]]

# km **2 / s ** 2
e_pot_cen = [phi for phi in s_cen["phi"]]
e_kin_cen = [0.5 * (vxi**2 + vyi**2 + vzi**2) for vxi, vyi, vzi in zip(vx_cen, vy_cen, vz_cen)]
e_tot_cen = [e_kini + e_poti for e_kini, e_poti in zip(e_kin_cen, e_pot_cen)]

e_pot_com = [phi for phi in s_com["phi"]]
e_kin_com = [0.5 * (vxi**2 + vyi**2 + vzi**2) for vxi, vyi, vzi in zip(vx_com, vy_com, vz_com)]
e_tot_com = [e_kini + e_poti for e_kini, e_poti in zip(e_kin_com, e_pot_com)]

# kpc km / s
l_z_cen = [rxi * vyi - ryi * vxi for rxi, ryi, vxi, vyi in zip(x_cen, y_cen, vx_cen, vy_cen)]

l_z_com = [rxi * vyi - ryi * vxi for rxi, ryi, vxi, vyi in zip(x_com, y_com, vx_com, vy_com)]

ax1.scatter(s_cen["r"].in_units("kpc"), np.array(s_cen["phi"]) * 10**-5, s=2, c="k", alpha=0.1)
ax1.scatter(s_com["r"].in_units("kpc"), np.array(s_com["phi"]) * 10**-5, s=2, c="magenta", alpha=0.1)
ax1.set_xlabel("r (kpc)")
ax1.set_ylabel(r"E$_{\phi}$ " + "($10^{5}$ $km^{2}$ $s^{-2}$)")

ax3.scatter(np.array(l_z_cen) * 10**-3, np.array(e_tot_cen) * 10**-5, s=2, c="k", alpha=0.1)
ax3.scatter(np.array(l_z_com) * 10**-3, np.array(e_tot_com) * 10**-5, s=2, c="magenta", alpha=0.1)
ax3.set_xlabel("$L_{z}$ ($10^{3}$ $kpc$ $km$ $s^{-1}$)")
ax3.set_ylabel("E ($10^{5}$ $km^{2}$ $s^{-2}$)")

ax2.axis("off")

ax0.scatter(x_com, y_com, c="magenta", s=2)

plt.show()
