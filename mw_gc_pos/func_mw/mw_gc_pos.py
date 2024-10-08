import matplotlib.pyplot as plt
import numpy as np
from astropy.table import Table
from matplotlib.patches import Ellipse


def mw_gc_pos(data_table: Table, plot_show: bool = False, plot_save: bool = False):
    # https://gea.esac.esa.int/archive/documentation/GDR3/Gaia_archive/chap_datamodel/sec_dm_performance_verification/ssec_dm_chemical_cartography.html

    x = -np.array(data_table["x_gc"])  # -ve as sign convention difference between gc catalogue and astropy
    y = np.array(data_table["y_gc"])
    z = np.array(data_table["z_gc"])

    size_lims = 40
    ticks = np.linspace(-size_lims, size_lims, 5)

    select_min_xy = 25  # kpc
    select_min_xz = 2  # kpc

    size = 2
    lw = 1
    zord = 10
    ls = "-"
    colour = "tab:blue"
    flag_colour = "red"

    fig, axs = plt.subplots(2, 2, figsize=(6, 6))
    plt.subplots_adjust(wspace=0, hspace=0)

    axs[0, 1].axis("off")

    xy_lim = plt.Circle(
        (0, 0), select_min_xy, fill=False, edgecolor="r", linestyle=ls, linewidth=lw, zorder=zord
    )

    xz_lim = Ellipse(
        xy=(0, 0),
        width=select_min_xy * 2,
        height=select_min_xz * 2,
        fill=False,
        edgecolor="r",
        linestyle=ls,
        linewidth=lw,
        zorder=zord,
    )

    yz_lim = Ellipse(
        xy=(0, 0),
        width=select_min_xy * 2,
        height=select_min_xz * 2,
        fill=False,
        edgecolor="r",
        linestyle=ls,
        linewidth=lw,
        zorder=zord,
    )

    rad_xy = (x**2 / (select_min_xy) ** 2) + (y**2 / (select_min_xy) ** 2)
    colors_xy = np.array([colour] * len(rad_xy))
    colors_xy[np.where(rad_xy <= 1.0)[0]] = flag_colour

    # axs[0, 0].scatter(x, y, c=colors_xy, s=size)

    rad_xz = (x**2 / (select_min_xy) ** 2) + (z**2 / (select_min_xz) ** 2)
    colors_xz = np.array([colour] * len(rad_xz))
    colors_xz[np.where(rad_xz <= 1.0)[0]] = flag_colour

    # axs[1, 0].scatter(x, z, c=colors_xz, s=size)

    rad_yz = (x**2 / (select_min_xy) ** 2) + (y**2 / (select_min_xz) ** 2)
    colors_yz = np.array([colour] * len(rad_yz))
    colors_yz[np.where(rad_xz <= 1.0)[0]] = flag_colour

    # axs[1, 1].scatter(y, z, c=colors_yz, s=size)

    axs[0, 0].add_patch(xy_lim)
    axs[1, 0].add_patch(xz_lim)
    axs[1, 1].add_patch(yz_lim)

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

    axs[1, 0].set_yticks(ticks[:-1])
    axs[1, 0].set_xticks(ticks[:-1])

    req_fit = [
        1 if (xc == flag_colour and yc == flag_colour and zc == flag_colour) else 0
        for xc, yc, zc in zip(colors_xy, colors_xz, colors_yz)
    ]

    for i in range(0, len(req_fit)):
        if req_fit[i] == 1:
            axs[0, 0].scatter(x[i], y[i], c=flag_colour, s=size)
            axs[1, 0].scatter(x[i], z[i], c=flag_colour, s=size)
            axs[1, 1].scatter(y[i], z[i], c=flag_colour, s=size)

        else:
            axs[0, 0].scatter(x[i], y[i], c=colour, s=size)
            axs[1, 0].scatter(x[i], z[i], c=colour, s=size)
            axs[1, 1].scatter(y[i], z[i], c=colour, s=size)

    data_table["pos_fit"] = req_fit

    data_table.write("mw_gc_pos/d_exp_mw/orbit_details_mod.csv", overwrite=True, delimiter=",")

    # check with Sarah the sign on X_sun
    x_s, y_s, z_s = -8.249, 0, 0.0208
    c_s = "green"
    s_s = 20

    axs[0, 0].scatter(x_s, y_s, marker="*", c=c_s, s=s_s)
    axs[1, 0].scatter(x_s, z_s, marker="*", c=c_s, s=s_s)
    axs[1, 1].scatter(y_s, z_s, marker="*", c=c_s, s=s_s)

    axs[0, 0].plot([1.9, 1.9], [-50, 50], c="k", ls="dashed")
    axs[0, 0].plot([-1.9, -1.9], [-50, 50], c="k", ls="dashed")

    axs[0, 0].plot([-50, 50], [1.9, 1.9], c="k", ls="dashed")
    axs[0, 0].plot([-50, 50], [-1.9, -1.9], c="k", ls="dashed")

    if plot_show:
        plt.show()

    if plot_save:
        # save figure
        PRINT_DIR = "mw_gc_pos/figs_mw/"
        FIG_NAME = "mw_gc_pos.pdf"
        fig.savefig(PRINT_DIR + FIG_NAME)
