import matplotlib.pyplot as plt
import numpy as np
from astropy.table import Table

data_table = Table.read("mw_gc_pos/d_imp_mw/orbit_details.csv")

vx_gc = data_table["u"]
vy_gc = data_table["v"]
vz_gc = data_table["w"]

x = -np.array(data_table["x_gc"])  # -ve as sign convention difference between gc catalogue and astropy
y = np.array(data_table["y_gc"])
z = np.array(data_table["z_gc"])

phi = np.arctan(y / x)

v_rho = vx_gc * np.cos(phi) + vy_gc * np.sin(phi)
v_phi = -vx_gc * np.sin(phi) + vy_gc * np.cos(phi)

r = np.sqrt(x**2 + y**2 + z**2)
rho = np.sqrt(x**2 + y**2)


v_lim = 500
fig, ax = plt.subplots(nrows=3, ncols=1)

ax[0].scatter(rho, v_phi)
ax[0].set(xlabel="r (kpc)", ylabel="v_phi (km/s)")
ax[0].set_xlim([0, 30])
ax[0].set_ylim([-v_lim, v_lim])

ax[1].scatter(rho, vz_gc)
ax[1].set(xlabel="r (kpc)", ylabel="v_z (km/s)")
ax[1].set_xlim([0, 30])
ax[1].set_ylim([-v_lim, v_lim])

ax[2].scatter(rho, v_rho)
ax[2].set(xlabel="r (kpc)", ylabel="v_r (km/s)")
ax[2].set_xlim([0, 30])
ax[2].set_ylim([-v_lim, v_lim])

plt.show()
