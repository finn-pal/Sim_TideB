import json

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pynbody
import pynbody.plot.sph as sph
from data_pull import data_pull
from kinematics import filter_particles, get_kinematics
from matplotlib.animation import PillowWriter
from mpl_toolkits.axes_grid1 import make_axes_locatable


def trace_xy_gif(init_time, timestep, num_timestep, gc_list, gif_name="TideB_Migration_xy.gif"):
    # data folder location
    # DATA_FLDRPTH = "/Users/z5114326/Desktop/Tets/"
    DATA_FLDRPTH = "/Volumes/My Passport for Mac/TideB/"

    BASE_FILE_0 = "GLX.000000"
    BASE_FILE_1 = "GLX.00000"

    INIT_FILE_0 = BASE_FILE_0[: -len(str(init_time))] + str(init_time)
    INIT_FILE_1 = BASE_FILE_1[: -len(str(init_time))] + str(init_time)

    metadata = dict(title="TideB", artist="Finn")
    writer = PillowWriter(fps=8, metadata=metadata)

    fig, _ = plt.subplots(nrows=1, ncols=1, figsize=(8, 8))

    i = 0

    if int(init_time) < 610:
        init_file_num = INIT_FILE_0.split(".")[-1]
    else:
        init_file_num = INIT_FILE_1.split(".")[-1]

    next_time_num = init_file_num

    fig = plt.figure(figsize=(12, 10))

    data_hold = {}
    data_hold["x_dict"] = {}
    data_hold["y_dict"] = {}

    for j in range(0, len(gc_list)):
        data_hold["x_dict"][j] = []
        data_hold["y_dict"][j] = []

    with writer.saving(fig, gif_name, 100):
        while i <= num_timestep:
            if int(next_time_num) < 610:
                next_file = INIT_FILE_0[: -len(next_time_num)] + next_time_num

            else:
                next_file = INIT_FILE_1[: -len(next_time_num)] + next_time_num

            filepath = DATA_FLDRPTH + next_file

            print(next_file)

            s = pynbody.load(filepath)
            s_updt = filter_particles(s, part_type="stars", part_select="get_lst", par_lst=gc_list)
            s_updt.physical_units()
            t_now = s_updt.properties["time"].in_units("Myr")
            timestr = str(int(np.round(float(t_now), 1)))

            s_phi = filter_particles(s, part_type="stars", part_select="get_all")
            s_phi.physical_units()

            phi_min = np.min(s_phi[s_phi["r"] < 15]["phi"])
            x_com = s_phi[s_phi["phi"] == phi_min]["x"]
            y_com = s_phi[s_phi["phi"] == phi_min]["y"]

            ################

            plt.xlim(-25, 25)
            plt.xlabel("x [kpc]")

            plt.ylim(-25, 25)
            plt.ylabel("y [kpc]")

            x = s_updt["x"]
            y = s_updt["y"]

            for j in range(0, len(gc_list)):
                data_hold["x_dict"][j].append(x[j])
                data_hold["y_dict"][j].append(y[j])

                plt.plot(data_hold["x_dict"][j], data_hold["y_dict"][j], c="grey")

            plt.scatter(x, y, c="blue")
            plt.scatter(x_com, y_com, c="red", s=40)

            plt.text(20, 20, timestr + " Myr", ha="right", fontsize=20)

            writer.grab_frame()
            fig.clear()

            ################

            # next loop step
            past_file_num = next_time_num
            next_time_num = str(int(past_file_num) + timestep)
            i += 1

    # print(data_hold)


with open("gc_list.json") as json_file:
    gc_list = json.load(json_file)

iteration = gc_list["iteration1"]
# iteration = iteration[:2]

trace_xy_gif(10, 10, 99, iteration, gif_name="TideB_Migration_xy_test.gif")
