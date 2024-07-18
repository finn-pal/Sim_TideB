import astropy.coordinates as coord
import astropy.units as u
import matplotlib.pyplot as plt
from astropy.coordinates import CylindricalRepresentation
from astropy.table import Table

data_table = Table.read("mw_gc_pos/d_imp_mw/orbit_details.csv")
sigma_z_thick = 41.45

# https://iopscience.iop.org/article/10.3847/1538-3881/ab9813


def mw_gc_vel(
    data_table: Table, sigma_z_thick: float = 41.45, plot_show: bool = False, plot_save: bool = False
):
    ls_vect = []

    size = 2
    lw = 1.5
    ls = "--"
    colour = "tab:blue"
    flag_colour = "red"

    for data in data_table:
        x_gc = data["x_gc"]
        y_gc = data["y_gc"]
        z_gc = data["z_gc"]

        vx_gc = data["u"]
        vy_gc = data["v"]
        vz_gc = data["w"]

        gc_frame = coord.Galactocentric(
            x=x_gc * u.kpc,
            y=y_gc * u.kpc,
            z=z_gc * u.kpc,
            v_x=vx_gc * u.km / u.s,
            v_y=vy_gc * u.km / u.s,
            v_z=vz_gc * u.km / u.s,
            representation_type="cartesian",
            differential_type="cartesian",
        )

        gc_pos_c = gc_frame.represent_as(CylindricalRepresentation)

        vr = gc_pos_c.differentials["s"].d_rho.to(u.km / u.s)
        vphi = (gc_pos_c.rho * gc_pos_c.differentials["s"].d_phi).to(u.km / u.s, u.dimensionless_angles())
        vz = gc_pos_c.differentials["s"].d_z.to(u.km / u.s)

        vect = [gc_pos_c.rho, gc_pos_c.phi, gc_pos_c.z, vr, vphi, vz]
        ls_vect.append(vect)

    data_table["rho_gc"] = [vect[0].value for vect in ls_vect]
    data_table["phi_gc"] = [vect[1].value for vect in ls_vect]
    data_table["z_gc"] = [vect[2].value for vect in ls_vect]
    data_table["vrho_gc"] = [vect[3].value for vect in ls_vect]
    data_table["vphi_gc"] = [vect[4].value for vect in ls_vect]
    data_table["vz_gc"] = [vect[5].value for vect in ls_vect]

    data_table["rho_gc"].units = u.kpc
    data_table["phi_gc"].units = u.rad
    data_table["z_gc"].units = u.kpc
    data_table["vrho_gc"].units = u.km / u.s
    data_table["vphi_gc"].units = u.km / u.s
    data_table["vz_gc"].units = u.km / u.s

    vel_fit = [
        1 if (v_phi >= 0 and v_z >= -sigma_z_thick and v_z <= sigma_z_thick) else 0
        for v_phi, v_z in zip(data_table["vphi_gc"], data_table["vz_gc"])
    ]

    data_table["vel_fit"] = vel_fit

    # Writes the new table with details in csv format
    data_table.write("mw_gc_pos/d_exp_mw/orbit_details_mod.csv", overwrite=True, delimiter=",")

    fig, axs = plt.subplots(figsize=(6, 6))

    x = data_table["vphi_gc"]
    y = data_table["vz_gc"]

    for i in range(0, len(vel_fit)):
        if vel_fit[i] == 1:
            axs.scatter(x[i], y[i], c=flag_colour, s=size)

        else:
            axs.scatter(x[i], y[i], c=colour, s=size)

    axs.plot([0, 0], [-sigma_z_thick, sigma_z_thick], c=flag_colour, ls=ls, lw=lw)
    axs.plot([0, 350], [sigma_z_thick, sigma_z_thick], c=flag_colour, ls=ls, lw=lw)
    axs.plot([0, 350], [-sigma_z_thick, -sigma_z_thick], c=flag_colour, ls=ls, lw=lw)

    axs.set(xlabel="$v_{\\phi}$ [km/s]", ylabel="$v_{z}$ [km/s]")
    axs.set(xlim=[-350, 350], ylim=[-250, 250])

    axs.text(
        1.01,
        0.405,
        "$-\\sigma_z$",
        transform=axs.transAxes,
        horizontalalignment="left",
    )

    axs.text(
        1.01,
        0.57,
        "$+\\sigma_z$",
        transform=axs.transAxes,
        horizontalalignment="left",
    )

    if plot_show:
        plt.show()

    if plot_save:
        # save figure
        PRINT_DIR = "mw_gc_pos/figs_mw/"
        FIG_NAME = "mw_gc_vel.pdf"
        fig.savefig(PRINT_DIR + FIG_NAME)
