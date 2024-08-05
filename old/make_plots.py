import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pynbody.plot.sph as sph

# from src.comp_pos import com_star_pos
from comp_pos import com_star_pos


def plt_stellar_density(
    snapshot,
    ax,
    vmin: float = 3e-4,
    vmax: float = 8e-2,
    plt_com: bool = True,
    comp_col: str = "magenta",
    plt_show: bool = False,
    plt_save: bool = False,
    save_name: str = "stellar_plot_test",
):
    params = {"font.family": "serif", "mathtext.fontset": "stix"}
    matplotlib.rcParams.update(params)

    t_now = snapshot.properties["time"].in_units("Myr")
    timestr = str(np.round(float(t_now), 1))

    # _, ax = plt.subplots(nrows=1, ncols=1)

    sph.image(
        snapshot.s,
        qty="rho",
        width="200 kpc",
        cmap="Blues",
        units="g cm^-2",
        show_cbar=True,
        # subplot=ax,
        vmin=vmin,
        vmax=vmax,
    )

    ax.set_xlabel("$x \\;{\\rm [kpc]}$", fontsize=15)
    ax.set_ylabel("$y \\;{\\rm [kpc]}$", fontsize=15)
    ax.annotate(timestr + "Myr", xy=(0.7, 0.9), xycoords="axes fraction", color="white", fontsize=13)

    if plt_com:
        test = com_star_pos(snapshot)
        ax.scatter(test["x"], test["y"], c=comp_col, s=2)

    if plt_show:
        plt.show()

    if plt_save:
        plt.savefig("reports/figures/" + save_name)

    return ax
