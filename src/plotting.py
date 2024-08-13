import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pynbody
import pynbody.plot.sph as sph
from data_pull import data_pull
from kinematics import filter_particles, get_kinematics
from matplotlib.animation import PillowWriter
from mpl_toolkits.axes_grid1 import make_axes_locatable


def make_plot(s):
    params = {"font.family": "serif", "mathtext.fontset": "stix", "font.size": 12}
    matplotlib.rcParams.update(params)

    t_now = s.properties["time"].in_units("Myr")
    timestr = str(int(np.round(float(t_now), 1)))

    vmin = 1e-2
    vmax = 1e5
    cmap = "bone"

    c_cen = "k"
    c_com = "magenta"
    c_cap = "lime"
    c_gc = "gold"

    com_min = 1008463671
    com_max = 1008473670

    cap_part = 1008464975

    gc_ls = [
        1008007175,
        1007618599,
        1007620723,
        1008252387,
        1007660890,
        1008415021,
        1008444910,
        1007760086,
        1008444252,
        1008089944,
        1008368081,
        1008292615,
        1008347636,
    ]

    s_cen = filter_particles(s, part_type="stars", part_select="exc_rng", rng_min=com_min, rng_max=com_max)
    s_com = filter_particles(s, part_type="stars", part_select="get_rng", rng_min=com_min, rng_max=com_max)
    s_cap = filter_particles(s, part_type="stars", part_select="get_one", part_id=cap_part)
    s_gc = filter_particles(s, part_type="stars", part_select="get_lst", par_lst=gc_ls)

    k_cen = get_kinematics(s_cen)
    k_com = get_kinematics(s_com)
    k_cap = get_kinematics(s_cap)
    k_gc = get_kinematics(s_gc)

    fig_shape = (4, 2)

    plt.subplots_adjust(wspace=0.4, hspace=0.5)

    ax0 = plt.subplot2grid(shape=fig_shape, loc=(0, 0))
    ax1 = plt.subplot2grid(shape=fig_shape, loc=(0, 1), rowspan=2)
    ax2 = plt.subplot2grid(shape=fig_shape, loc=(1, 0), rowspan=2)
    ax3 = plt.subplot2grid(shape=fig_shape, loc=(2, 1), rowspan=2)
    ax4 = plt.subplot2grid(shape=fig_shape, loc=(3, 0))

    # xy plot

    sph.image(
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

    ax2.scatter(k_com["x"], k_com["y"], c=c_com, s=10, alpha=0.2)
    ax2.scatter(k_cap["x"], k_cap["y"], c=c_cap, s=20)
    ax2.scatter(k_gc["x"], k_gc["y"], c=c_gc, s=20)

    ticks = np.linspace(-100, 100, 5)
    ax2.set_facecolor("black")
    ax2.set_xlabel("$x \\;{\\rm [kpc]}$", fontsize=13)
    ax2.set_ylabel("$y \\;{\\rm [kpc]}$", fontsize=13, labelpad=-10)
    ax2.set(xticks=ticks, yticks=ticks)

    ax2.annotate(
        timestr + " Myr",
        xy=(0.35, 0.1),
        xycoords="axes fraction",
        color="white",
        fontsize=13,
        ha="right",
    )

    # iom
    vmin_iom = 0
    vmax_iom = 50000

    im_iom = ax1.hist2d(
        -np.array(k_cen["lz"]) * 10**-3,
        np.array(k_cen["e_tot"]) * 10**-5,
        bins=50,
        cmap="bone_r",
        vmin=vmin_iom,
        vmax=vmax_iom,
    )

    ax1.scatter(-np.array(k_com["lz"]) * 10**-3, np.array(k_com["e_tot"]) * 10**-5, s=2, c=c_com, alpha=0.1)
    ax1.scatter(-np.array(k_cap["lz"]) * 10**-3, np.array(k_cap["e_tot"]) * 10**-5, s=30, c=c_cap)
    ax1.scatter(-np.array(k_gc["lz"]) * 10**-3, np.array(k_gc["e_tot"]) * 10**-5, s=30, c=c_gc)

    clb = plt.colorbar(
        im_iom[3],
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
    ax1.set(xlim=[-17.5, 17.5], ylim=[-3.25, 0.75])

    # e_pot

    ax3.scatter(s_cen["r"].in_units("kpc"), np.array(s_cen["phi"]) * 10**-5, s=2, c=c_cen, alpha=0.1)
    ax3.scatter(s_com["r"].in_units("kpc"), np.array(s_com["phi"]) * 10**-5, s=2, c=c_com, alpha=0.1)
    ax3.scatter(s_cap["r"].in_units("kpc"), np.array(s_cap["phi"]) * 10**-5, s=30, c=c_cap)
    ax3.scatter(s_gc["r"].in_units("kpc"), np.array(s_gc["phi"]) * 10**-5, s=30, c=c_gc)

    ax3.set_xlabel("r (kpc)")
    ax3.set_ylabel(r"E$_{\phi}$ " + "($10^{5}$ $km^{2}$ $s^{-2}$)")
    ax3.set(xlim=[-10, 350], ylim=[-3.5, 0])

    # xz plot

    s.rotate_x(270)

    sph.image(
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

    ax0.scatter(k_com["x"], k_com["z"], c=c_com, s=10, alpha=0.2)
    ax0.scatter(k_cap["x"], k_cap["z"], c=c_cap, s=20)
    ax0.scatter(k_gc["x"], k_gc["z"], c=c_gc, s=20)

    ax0.set_xlim([-100, 100])
    ax0.set_ylim([-30, 30])
    ax0.set(xticks=ticks, yticks=[-20, 0, 20])
    ax0.xaxis.set_visible(False)

    ax0.set_facecolor("black")
    ax0.set_ylabel("$z \\;{\\rm [kpc]}$", fontsize=13, labelpad=0)

    pos2 = ax2.get_position()
    ax0.set_position([pos2.x0, 0.57, pos2.width, pos2.height])
    divider = make_axes_locatable(ax0)

    cax = divider.append_axes("top", size="20%", pad=0.10)
    im_c = ax4.imshow(np.array([[np.log10(vmin), np.log10(vmax)]]), cmap=cmap, origin="lower")
    im_c.set_visible(False)

    plt.colorbar(im_c, cax=cax, orientation="horizontal")

    cax.xaxis.tick_top()
    cax.xaxis.set_label_position("top")
    cax.set_xticks([-2, -1, 0, 1, 2, 3, 4, 5])
    cax.set_xlabel("log$_{10}$ Stellar Density [M$_\u2609$ pc$^{-2}$]", labelpad=10)

    # axis off
    ax4.axis("off")


def make_gif(init_time, timestep, num_timestep, gif_name="TideB_Default"):
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

    with writer.saving(fig, gif_name, 100):
        while i <= num_timestep:
            if int(next_time_num) < 610:
                next_file = INIT_FILE_0[: -len(next_time_num)] + next_time_num

            else:
                next_file = INIT_FILE_1[: -len(next_time_num)] + next_time_num

            filepath = DATA_FLDRPTH + next_file

            print(next_file)

            # do code looping here
            s = pynbody.load(filepath)
            s.physical_units()

            ################

            make_plot(s)

            ################

            writer.grab_frame()
            fig.clear()

            # next loop step
            past_file_num = next_time_num
            next_time_num = str(int(past_file_num) + timestep)
            i += 1


########################################################################################################


def migration_plot(s_init, s_updt):
    t_now = s_updt.properties["time"].in_units("Myr")
    timestr = str(int(np.round(float(t_now), 1)))

    rlim = 25
    elim_l = -3.5
    elim_u = 1
    llim = 20

    lw = 0.5
    s = 10

    r_init = s_init["r"]
    e_init = s_init["te"]
    l_init = s_init["jz"]

    r_updt = s_updt["r"]
    e_updt = s_updt["te"]
    l_updt = s_updt["jz"]

    fig_shape = (2, 2)

    ax0 = plt.subplot2grid(shape=fig_shape, loc=(0, 0))
    ax1 = plt.subplot2grid(shape=fig_shape, loc=(0, 1))
    ax2 = plt.subplot2grid(shape=fig_shape, loc=(1, 0))

    ax0.annotate(
        timestr + " Myr",
        xy=(0.2, 0.9),
        xycoords="axes fraction",
        color="black",
        fontsize=13,
        ha="right",
    )

    ax0.plot([0, rlim], [0, rlim], c="k", ls="dashed", lw=lw)
    ax0.scatter(r_init, r_updt, s=s, c="blue")
    ax0.set(xlabel="r$_{init}$ [kpc]", ylabel="r$_{update}$ [kpc]")
    ax0.set(xlim=[0, rlim], ylim=[0, rlim])

    ax1.plot([-llim, llim], [-llim, llim], c="k", ls="dashed", lw=lw)
    ax1.scatter(-np.array(l_init) * 10**-3, -np.array(l_updt) * 10**-3, s=s, c="blue")
    ax1.set(
        xlabel="$L_{z, init}$ ($10^{3}$ $kpc$ $km$ $s^{-1}$)",
        ylabel="$L_{z, update}$ ($10^{3}$ $kpc$ $km$ $s^{-1}$)",
    )
    ax1.set(xlim=[-llim, llim], ylim=[-llim, llim])

    ax2.plot([elim_l, elim_u], [elim_l, elim_u], c="k", ls="dashed", lw=lw)
    ax2.scatter(np.array(e_init) * 10**-5, np.array(e_updt) * 10**-5, s=s, c="blue")
    ax2.set(
        xlabel="E$_{init}$ ($10^{5} km^{2} s^{-2}$)",
        ylabel="E$_{update}$ ($10^{5} km^{2} s^{-2}$)",
    )
    ax2.set(xlim=[elim_l, elim_u], ylim=[elim_l, elim_u])


def migration_gif(init_time, timestep, num_timestep, iteration, gif_name="TideB_Migration"):
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

    s_init = data_pull(init_time)
    s_init = filter_particles(s_init, part_type="stars", part_select="get_lst", par_lst=iteration)
    s_init.physical_units()

    fig = plt.figure(figsize=(12, 10))

    with writer.saving(fig, gif_name, 100):
        while i <= num_timestep:
            if int(next_time_num) < 610:
                next_file = INIT_FILE_0[: -len(next_time_num)] + next_time_num

            else:
                next_file = INIT_FILE_1[: -len(next_time_num)] + next_time_num

            filepath = DATA_FLDRPTH + next_file

            print(next_file)

            s_updt = pynbody.load(filepath)
            s_updt = filter_particles(s_updt, part_type="stars", part_select="get_lst", par_lst=iteration)
            s_updt.physical_units()

            ################

            migration_plot(s_init, s_updt)

            ################

            writer.grab_frame()
            fig.clear()

            # next loop step
            past_file_num = next_time_num
            next_time_num = str(int(past_file_num) + timestep)
            i += 1


def migration_plot_comb(s_init_1, s_updt_1, s_init_2, s_updt_2, c1="blue", c2="red"):
    t_now = s_updt_1.properties["time"].in_units("Myr")
    timestr = str(int(np.round(float(t_now), 1)))

    rlim = 25
    elim_l = -3.5
    elim_u = 1
    llim = 20

    lw = 0.5
    s = 10

    r_init_1 = s_init_1["r"]
    e_init_1 = s_init_1["te"]
    l_init_1 = s_init_1["jz"]

    r_updt_1 = s_updt_1["r"]
    e_updt_1 = s_updt_1["te"]
    l_updt_1 = s_updt_1["jz"]

    r_init_2 = s_init_2["r"]
    e_init_2 = s_init_2["te"]
    l_init_2 = s_init_2["jz"]

    r_updt_2 = s_updt_2["r"]
    e_updt_2 = s_updt_2["te"]
    l_updt_2 = s_updt_2["jz"]

    fig_shape = (2, 2)

    ax0 = plt.subplot2grid(shape=fig_shape, loc=(0, 0))
    ax1 = plt.subplot2grid(shape=fig_shape, loc=(0, 1))
    ax2 = plt.subplot2grid(shape=fig_shape, loc=(1, 0))

    ax0.annotate(
        timestr + " Myr",
        xy=(0.2, 0.9),
        xycoords="axes fraction",
        color="black",
        fontsize=13,
        ha="right",
    )

    ax0.plot([0, rlim], [0, rlim], c="k", ls="dashed", lw=lw)
    ax0.scatter(r_init_1, r_updt_1, s=s, c=c1)
    ax0.scatter(r_init_2, r_updt_2, s=s, c=c2)
    ax0.set(xlabel="r$_{init}$ [kpc]", ylabel="r$_{update}$ [kpc]")
    ax0.set(xlim=[0, rlim], ylim=[0, rlim])

    ax1.plot([-llim, llim], [-llim, llim], c="k", ls="dashed", lw=lw)
    ax1.scatter(-np.array(l_init_1) * 10**-3, -np.array(l_updt_1) * 10**-3, s=s, c=c1)
    ax1.scatter(-np.array(l_init_2) * 10**-3, -np.array(l_updt_2) * 10**-3, s=s, c=c2)
    ax1.set(
        xlabel="$L_{z, init}$ ($10^{3}$ $kpc$ $km$ $s^{-1}$)",
        ylabel="$L_{z, update}$ ($10^{3}$ $kpc$ $km$ $s^{-1}$)",
    )
    ax1.set(xlim=[-llim, llim], ylim=[-llim, llim])

    ax2.plot([elim_l, elim_u], [elim_l, elim_u], c="k", ls="dashed", lw=lw)
    ax2.scatter(np.array(e_init_1) * 10**-5, np.array(e_updt_1) * 10**-5, s=s, c=c1)
    ax2.scatter(np.array(e_init_2) * 10**-5, np.array(e_updt_2) * 10**-5, s=s, c=c2)
    ax2.set(
        xlabel="E$_{init}$ ($10^{5} km^{2} s^{-2}$)",
        ylabel="E$_{update}$ ($10^{5} km^{2} s^{-2}$)",
    )
    ax2.set(xlim=[elim_l, elim_u], ylim=[elim_l, elim_u])


def migration_gif_comb(init_time, timestep, num_timestep, gc_list, gif_name="TideB_Migration_Comb"):
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

    iteration1 = gc_list["iteration1"]
    iteration2 = gc_list["iteration2"]

    s_init_1 = data_pull(init_time)
    s_init_1 = filter_particles(s_init_1, part_type="stars", part_select="get_lst", par_lst=iteration1)
    s_init_1.physical_units()

    s_init_2 = data_pull(init_time)
    s_init_2 = filter_particles(s_init_2, part_type="stars", part_select="get_lst", par_lst=iteration2)
    s_init_2.physical_units()

    fig = plt.figure(figsize=(12, 10))

    with writer.saving(fig, gif_name, 100):
        while i <= num_timestep:
            if int(next_time_num) < 610:
                next_file = INIT_FILE_0[: -len(next_time_num)] + next_time_num

            else:
                next_file = INIT_FILE_1[: -len(next_time_num)] + next_time_num

            filepath = DATA_FLDRPTH + next_file

            print(next_file)

            s_updt_1 = pynbody.load(filepath)
            s_updt_1 = filter_particles(
                s_updt_1, part_type="stars", part_select="get_lst", par_lst=iteration1
            )
            s_updt_1.physical_units()

            s_updt_2 = pynbody.load(filepath)
            s_updt_2 = filter_particles(
                s_updt_2, part_type="stars", part_select="get_lst", par_lst=iteration2
            )
            s_updt_2.physical_units()

            ################

            migration_plot_comb(s_init_1, s_updt_1, s_init_2, s_updt_2, c1="blue", c2="red")

            ################

            writer.grab_frame()
            fig.clear()

            # next loop step
            past_file_num = next_time_num
            next_time_num = str(int(past_file_num) + timestep)
            i += 1
