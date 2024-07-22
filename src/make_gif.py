import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pynbody
import pynbody.plot.sph as sph
from comp_pos import com_star_pos
from make_plots import plt_stellar_density
from matplotlib.animation import PillowWriter

# data folder location
# DATA_FLDRPTH = "/Users/z5114326/Desktop/Tets/"
DATA_FLDRPTH = "/Volumes/My Passport for Mac/TideB/"

# data loop details
INIT_TIME = 20
TIMESTEP = 20
NUM_TIMESTEP = 10

BASE_FILE = "GLX.000000"
INIT_FILE = BASE_FILE[: -len(str(INIT_TIME))] + str(INIT_TIME)

metadata = dict(title="Test", artist="Loser")
writer = PillowWriter(fps=1, metadata=metadata)

fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(8, 8))

i = 0

init_file_num = INIT_FILE.split(".")[-1]
next_time_num = init_file_num


with writer.saving(fig, "pop_test.gif", 100):
    while i <= NUM_TIMESTEP:
        next_file = INIT_FILE[: -len(next_time_num)] + next_time_num
        filepath = DATA_FLDRPTH + next_file
        print(next_file)

        # do code looping here
        s = pynbody.load(filepath)
        s.physical_units()
        t_now = s.properties["time"].in_units("Myr")
        timestr = str(np.round(float(t_now), 1))

        # plot
        # plt_stellar_density(s, ax)

        sph.image(
            s.s,
            qty="rho",
            width="200 kpc",
            cmap="Blues",
            units="g cm^-2",
            show_cbar=True,
        )

        test = com_star_pos(s)
        plt.scatter(test["x"], test["y"], c="magenta", s=2)

        writer.grab_frame()
        fig.clear()

        # next loop step
        past_file_num = next_time_num
        next_time_num = str(int(past_file_num) + TIMESTEP)
        i = i + 1

# ax = plt_stellar_density(s, plt_save=True)
