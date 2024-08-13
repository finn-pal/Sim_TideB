# %%
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pynbody
import pynbody.plot.sph as sph
from mpl_toolkits.axes_grid1 import make_axes_locatable

# data folder location
DATA_FLDRPTH = "/Users/z5114326/Desktop/Tets/"
# DATA_FLDRPTH = "/Volumes/My Passport for Mac/TideB/"

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


params = {"font.family": "serif", "mathtext.fontset": "stix", "font.size": 12}
matplotlib.rcParams.update(params)

# %%

vmin = 1e-2
vmax = 1e5
cmap = "bone"

fig = plt.figure(figsize=(12, 10))
plt.subplots_adjust(wspace=0.4, hspace=0.5)

fig_shape = (4, 2)

ax0 = plt.subplot2grid(shape=fig_shape, loc=(0, 0))
ax1 = plt.subplot2grid(shape=fig_shape, loc=(0, 1), rowspan=2)
ax2 = plt.subplot2grid(shape=fig_shape, loc=(1, 0), rowspan=2)
ax3 = plt.subplot2grid(shape=fig_shape, loc=(2, 1), rowspan=2)
ax4 = plt.subplot2grid(shape=fig_shape, loc=(3, 0))

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
    subplot=ax2,
)

ticks = np.linspace(-100, 100, 5)
ax2.set_facecolor("black")
ax2.set_xlabel("$x \\;{\\rm [kpc]}$", fontsize=13)
ax2.set_ylabel("$y \\;{\\rm [kpc]}$", fontsize=13, labelpad=-10)
ax2.set(xticks=ticks, yticks=ticks)


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

ax3.scatter(s_cen["r"].in_units("kpc"), np.array(s_cen["phi"]) * 10**-5, s=2, c="k", alpha=0.1)
ax3.scatter(s_com["r"].in_units("kpc"), np.array(s_com["phi"]) * 10**-5, s=2, c="magenta", alpha=0.1)
ax3.set_xlabel("r (kpc)")
ax3.set_ylabel(r"E$_{\phi}$ " + "($10^{5}$ $km^{2}$ $s^{-2}$)")

vmin_n = 0
vmax_n = 50000

im_h = ax1.hist2d(
    -np.array(l_z_cen) * 10**-3,
    np.array(e_tot_cen) * 10**-5,
    bins=50,
    cmap="bone_r",
    vmin=vmin_n,
    vmax=vmax_n,
)

clb = fig.colorbar(
    im_h[3],
    ax=ax1,
    format="%.0e",
    ticks=[0, 10000, 20000, 30000, 40000, 50000],
    pad=0.02,
    location="top",
)

clb.ax.set_xlabel("Number of Stellar Particles ($10^{4}$)", labelpad=10)
clb.ax.set_xticklabels([0, 1, 2, 3, 4, 5])

ax1.set_xlabel("$L_{z}$ ($10^{3}$ $kpc$ $km$ $s^{-1}$)")
ax1.set_ylabel("E ($10^{5}$ $km^{2}$ $s^{-2}$)")

pynbody.analysis.angmom.sideon(s)

im_s = sph.image(
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

ax0.set_ylim([-30, 30])
ax0.set(xticks=ticks, yticks=[-20, 0, 20])
ax0.xaxis.set_visible(False)

ax0.set_ylabel("$z \\;{\\rm [kpc]}$", fontsize=13, labelpad=0)

pos2 = ax2.get_position()
ax0.set_position([pos2.x0, 0.57, pos2.width, pos2.height])

divider = make_axes_locatable(ax0)
cax = divider.append_axes("top", size="20%", pad=0.10)

im_c = ax4.imshow(np.array([[np.log10(vmin), np.log10(vmax)]]), cmap=cmap, origin="lower")
im_c.set_visible(False)
fig.colorbar(im_c, cax=cax, orientation="horizontal")
cax.xaxis.tick_top()
cax.xaxis.set_label_position("top")
cax.set_xticks([-2, -1, 0, 1, 2, 3, 4, 5])
cax.set_xlabel("log$_{10}$ Stellar Density [M$_\u2609$ pc$^{-2}$]", labelpad=10)

ax4.axis("off")

ax0.scatter(x_com, z_com, c="magenta", s=2, alpha=0.2)
ax2.scatter(x_com, y_com, c="magenta", s=2, alpha=0.2)

# ax2.scatter(-np.array(l_z_cen) * 10**-3, np.array(e_tot_cen) * 10**-5, s=2, c="k", alpha=0.1)
ax1.scatter(-np.array(l_z_com) * 10**-3, np.array(e_tot_com) * 10**-5, s=2, c="magenta", alpha=0.2)

ax2.annotate(timestr + " Myr", xy=(0.1, 0.1), xycoords="axes fraction", color="white", fontsize=13)

# %%

plt.show()
