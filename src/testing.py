import matplotlib.pyplot as plt
import numpy as np
import pynbody
import pynbody.plot.sph as sph
from data_pull import data_pull
from kinematics import filter_particles, get_kinematics
from matplotlib.patches import Ellipse

# https://iopscience.iop.org/article/10.3847/1538-3881/ab5b0e

init_time = 10

s = data_pull(init_time, path="")

mw_dm_vir = 1.3e12  # Msol
mw_dm_vir_err = 0.3e12  # Msol

n_gc_log_mw = -9.58 + 0.99 * np.log10(mw_dm_vir)
n_gc_mw = 10**n_gc_log_mw

# print(n_gc_log_mw)
# print(n_gc_mw)

n_gc_log = -9.58 + 0.99 * np.log10(np.sum(s.dm["mass"]))
n_gc = 10**n_gc_log

# print(n_gc_log)
# print(n_gc)

com_min = 1008463671
com_max = 1008473670

s_cen = filter_particles(s, part_type="stars", part_select="exc_rng", rng_min=com_min, rng_max=com_max)
s_com = filter_particles(s, part_type="stars", part_select="get_rng", rng_min=com_min, rng_max=com_max)

test = s_cen[(s_cen["mass"] > 1e4) & (s_cen["r"] < 10)]
print(len(test))

##########################

size = 2
lw = 1
zord = 10
ls = "-"

size_lims = 40
ticks = np.linspace(-size_lims, size_lims, 5)

fig = plt.figure()

plt.scatter(s_cen["r"], s_cen["vphi"], s=2, c="blue")
plt.xlabel("r [kpc]")
plt.ylabel("v$_{phi}$ [km/s]")

fig, axs = plt.subplots(2, 2, figsize=(6, 6))
plt.subplots_adjust(wspace=0, hspace=0)

axs[0, 1].axis("off")

axs[1, 0].set_xlabel("x [kpc]")
axs[1, 1].set_xlabel("y [kpc]")
axs[0, 0].set_ylabel("y [kpc]")
axs[1, 0].set_ylabel("z [kpc]")

disk_scale = 2.470  # kpc

xy_lim = plt.Circle((0, 0), disk_scale, fill=False, edgecolor="r", linestyle=ls, linewidth=lw, zorder=zord)

axs[0, 0].add_patch(xy_lim)
axs[0, 0].scatter(s_cen["x"], s_cen["y"], s=size)

axs[1, 0].scatter(s_cen["x"], s_cen["z"], s=size)


for i, ax in enumerate(axs.flat):
    ax.set_xlim(-size_lims, size_lims)
    ax.set_ylim(-size_lims, size_lims)
    ax.set_xticks(ticks)
    ax.set_yticks(ticks)

axs[1, 0].set_xlabel("x [kpc]")
axs[1, 1].set_xlabel("y [kpc]")

axs[0, 0].set_ylabel("y [kpc]")
axs[1, 0].set_ylabel("z [kpc]")

axs[0, 0].set_xticklabels([])
axs[1, 1].set_yticklabels([])

plt.show()
