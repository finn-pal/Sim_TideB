import matplotlib.pyplot as plt


def plot_iom(data_table, circular_table, plot_show: bool = False, plot_save: bool = False):
    size = 2
    lw = 1
    ls = "--"
    colour = "tab:blue"
    flag_colour = "red"

    fig, axs = plt.subplots(figsize=(8, 8))

    x = data_table["l_z_base"] * 10**-3
    y = data_table["energy_base"] * 10**-5
    axs.scatter(x, y, c="blue", s=2)

    for i in range(0, len(x)):
        if (data_table["vel_fit"][i] == 1) and (data_table["pos_fit"][i] == 1):
            axs.scatter(x[i], y[i], c=flag_colour, s=size)

        else:
            axs.scatter(x[i], y[i], c=colour, s=size)

    # create bounds in IOM space using circular orbit information
    x_b_pos = circular_table["l_z_pos"] * 10**-3
    y_b_pos = circular_table["energy_pos"] * 10**-5

    x_b_neg = circular_table["l_z_neg"] * 10**-3
    y_b_neg = circular_table["energy_neg"] * 10**-5

    axs.plot(x_b_pos, y_b_pos, c="grey", ls=ls, lw=lw)
    axs.plot(x_b_neg, y_b_neg, c="grey", ls=ls, lw=lw)

    axs.set(
        xlim=[-5, 5],
        ylim=[-2.7, 0],
        xlabel="$L_{z}$ ($10^{3}$ $kpc$ $km$ $s^{-1}$)",
        ylabel="E ($10^{5}$ $km^{2}$ $s^{-2}$)",
    )

    disk_w = sum(
        [
            1 if pos_fit == 1 and vel_fit == 1 else 0
            for pos_fit, vel_fit in zip(data_table["pos_fit"], data_table["vel_fit"])
        ]
    )

    axs.text(
        0.8,
        0.5,
        f"{len(data_table["pos_fit"])} MW GC \n{disk_w} MW Disk GC",
        transform=axs.transAxes,
        horizontalalignment="left",
    )

    if plot_show:
        plt.show()

    if plot_save:
        # save figure
        PRINT_DIR = "mw_gc_pos/figs_mw/"
        FIG_NAME = "mw_gc_iom.pdf"
        fig.savefig(PRINT_DIR + FIG_NAME)
