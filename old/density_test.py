import matplotlib.pyplot as plt
import numpy as np
import pynbody

# data folder location
# DATA_FLDRPTH = "/Users/z5114326/Desktop/Tets/"
DATA_FLDRPTH = "/Volumes/My Passport for Mac/TideB/"

# data loop details
INIT_TIME = 600

BASE_FILE = "GLX.000000"
INIT_FILE = BASE_FILE[: -len(str(INIT_TIME))] + str(INIT_TIME)
filepath = DATA_FLDRPTH + INIT_FILE

print(INIT_FILE)

s = pynbody.load(filepath)
s.physical_units()
t_now = s.properties["time"].in_units("Myr")
timestr = str(np.round(float(t_now), 1))

x = [pos[0] for (pos) in s.s["pos"] if -100 <= pos[0] and pos[0] <= 100 and -100 <= pos[1] and pos[1] <= 100]
y = [pos[1] for (pos) in s.s["pos"] if -100 <= pos[0] and pos[0] <= 100 and -100 <= pos[1] and pos[1] <= 100]

x = np.array([pos[0] for pos in s.s["pos"]])
# y = np.array([pos[1] for pos in s.s["pos"]])
# z = np.array([mas for mas in s.s["mass"]])

x = s.s["x"]
y = s.s["y"]
ms = s.s["mass"]

L = 75  # length of box

dx = 1  # kpc
dy = 1  # kpc

nx = 2 * (int(L / dx))
ny = 2 * (int(L / dy))

xbin = np.linspace(-L, L, nx + 1)
ybin = np.linspace(-L, L, ny + 1)

x_test = []

ms_bin = np.zeros((nx, ny))
area = np.zeros((nx, ny))
rho_bin = np.zeros((nx, ny))

x_pc_sc = 1000  # kpc to pc
y_pc_sc = 1000  # kpc to pc

i = 0
j = 0
while i < nx:
    j = 0
    while j < ny:
        x1 = xbin[i]
        x2 = x1 + dx
        y1 = ybin[j]
        y2 = y1 + dy

        selgrid = (x1 < x) & (x < x2) & (y1 < y) & (y < y2)
        ms_bin[i, j] = np.sum(ms[selgrid])
        area[i, j] = (dx * x_pc_sc) * (dy * y_pc_sc)
        rho_bin[j, i] = ms_bin[i, j] / area[i, j]

        j += 1
    i += 1

vmin = 0
vmax = 4

fig, ax = plt.subplots()
im = ax.imshow(
    np.log10(rho_bin),
    origin="lower",
    extent=(-L, L, -L, L),
    cmap="bone",
    vmin=vmin,
    vmax=vmax,
)

com_id_min = 1008463671
com_id_max = 1008473670

x_c = [xi for xi, id in zip(s.s["x"], s.s["iord"]) if id >= com_id_min and id <= com_id_max]
y_c = [yi for yi, id in zip(s.s["y"], s.s["iord"]) if id >= com_id_min and id <= com_id_max]

ax.scatter(x_c, y_c, c="magenta", s=2)

fig.subplots_adjust(right=0.85)
cbar_ax = fig.add_axes([0.88, 0.15, 0.04, 0.7])
fig.colorbar(im, cax=cbar_ax)
ax.set_facecolor("black")


plt.show()
