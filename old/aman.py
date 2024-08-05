def halo_gal_plot():
    # loading in my data
    halogal_nh = np.loadtxt("./halogal_00906.dat_nocontam")
    halogal_nh = halogal_nh[halogal_nh[:, 4] >= 10**9.5]
    halogal_eagle = pd.read_csv("./halogal_392_eagle_v2.csv")
    halogal_tng = pd.read_csv("./halogal_95_tng_v2.csv")
    halogal_magneticum = pd.read_csv("./halogal_136_magneticum_v2.csv")
    # bins
    mstar_bins = np.linspace(9.5, 12.6, 25)
    mhalo_bins = np.linspace(10.3, 14.7, 25)
    bins = np.array([mhalo_bins, mstar_bins])
    # Observational SMHM relations
    ## old colours behroozi '#d0563f', moster '#3fb9d0'

    logmhalo_behroozi_z0p26, logmstar_behroozi_z0p26 = behroozi_smhm(0.26)
    logmhalo_behrozi_z0p05, logmstar_behroozi_z0p05 = behroozi_smhm(0.05)
    mhalo_moster_z0p26, mstar_moster_z0p26 = moster_smhm(0.26)
    mhalo_moster_z0p05, mstar_moster_z0p05 = moster_smhm(0.05)
    mhalo_hudson_z0p26, mstar_hudson_z0p26 = hudson_smhm(0.26)
    mhalo_hudson_z0p05, mstar_hudson_z0p05 = hudson_smhm(0.05)
    behroozi_colour = "#d0563f"
    moster_colour = "#3fd056"
    hudson_colour = "#563fd0"

    plt.close("all")
    cents_tng = halogal_tng["Subgroup ID"].values == 0
    cents_eagle = halogal_eagle["Subgroup ID"].values == 0
    cents_magneticum = halogal_magneticum["Subgroup ID"].values == 0
    cents_nh = halogal_nh[:, 1] == 1

    # tng_hist = np.histogram2d(
    # np.log10(halogal_tng[cents_tng]['M200'].values),
    # np.log10(halogal_tng[cents_tng]['Mstar Subfind'].values),
    #                             bins=bins,
    #                             density=True)
    eagle_hist = np.histogram2d(
        np.log10(halogal_eagle[cents_eagle]["M200"].values),
        np.log10(halogal_eagle[cents_eagle]["Mstar Subfind"].values),
        bins=bins,
        density=True,
    )
    cmap = mpl.cm.gray_r
    # norm = mpl.colors.Normalize(vmin=0, vmax=np.nanpercentile(tng_hist[0],95))
    norm = mpl.colors.PowerNorm(0.5, vmin=0, vmax=np.max(eagle_hist[0]))
    fig, axes = plt.subplots(1, 4, figsize=(10, 6), sharex=True, sharey=True)
    plt.subplots_adjust(wspace=0)
    for ax in axes:
        ax.plot(
            logmhalo_behroozi_z0p26,
            logmstar_behroozi_z0p26,
            color=behroozi_colour,
            ls="dotted",
            label="Behroozi et al. 13 (z=0.26)",
        )
        ax.plot(
            logmhalo_behrozi_z0p05,
            logmstar_behroozi_z0p05,
            color=behroozi_colour,
            ls="dashed",
            label="Behroozi et al. 13 (z=0.05)",
        )
        ax.plot(
            np.log10(mhalo_moster_z0p26),
            np.log10(mstar_moster_z0p26),
            color=moster_colour,
            ls="dotted",
            label="Moster et al. 13 (z=0.26)",
        )
        ax.plot(
            np.log10(mhalo_moster_z0p05),
            np.log10(mstar_moster_z0p05),
            color=moster_colour,
            ls="dashed",
            label="Moster et al. 13 (z=0.05)",
        )
        ax.plot(
            np.log10(mhalo_hudson_z0p26),
            np.log10(mstar_hudson_z0p26),
            color=hudson_colour,
            ls="dotted",
            label="Hudson et al. 15 (z=0.26)",
        )
        ax.plot(
            np.log10(mhalo_hudson_z0p05),
            np.log10(mstar_hudson_z0p05),
            color=hudson_colour,
            ls="dashed",
            label="Hudson et al. 15 (z=0.05)",
        )
    nh_hist = axes[0].hist2d(
        np.log10(halogal_nh[cents_nh, 2]),
        np.log10(halogal_nh[cents_nh, 4]),
        bins=bins,
        cmap=cmap,
        norm=norm,
        density=True,
    )
    nh_hist_raw_counts = np.histogram2d(
        np.log10(halogal_nh[cents_nh, 2]), np.log10(halogal_nh[cents_nh, 4]), bins=bins, density=False
    )
    suff_counts_nh = np.sum(nh_hist_raw_counts[0], axis=0) > 0
    median_mstar_nh = bin_medians(
        np.log10(halogal_nh[cents_nh, 4]), np.log10(halogal_nh[cents_nh, 2]), mhalo_bins
    )
    bin_mids = bins_values_to_histograms(mhalo_bins, np.empty(len(mhalo_bins) - 1))[0]

    axes[0].plot(
        bin_mids[suff_counts_nh], median_mstar_nh[suff_counts_nh], ls="solid", color="#ffb700", label="Median"
    )

    axes[0].legend(framealpha=0, fontsize=8)
    eagle_hist = axes[1].hist2d(
        np.log10(halogal_eagle[cents_eagle]["M200"].values),
        np.log10(halogal_eagle[cents_eagle]["Mstar Subfind"].values),
        bins=bins,
        cmap=cmap,
        norm=norm,
        density=True,
    )
    eagle_hist_raw_counts = np.histogram2d(
        np.log10(halogal_eagle[cents_eagle]["M200"].values),
        np.log10(halogal_eagle[cents_eagle]["Mstar Subfind"].values),
        bins=bins,
        density=False,
    )
    suff_counts_eagle = np.sum(eagle_hist_raw_counts[0], axis=0) > 0
    median_mstar_eagle = bin_medians(
        np.log10(halogal_eagle[cents_eagle]["Mstar Subfind"]),
        np.log10(halogal_eagle[cents_eagle]["M200"]),
        mhalo_bins,
    )
    axes[1].plot(
        bin_mids[suff_counts_eagle], median_mstar_eagle[suff_counts_eagle], ls="solid", color="#ffb700"
    )

    tng_hist = axes[2].hist2d(
        np.log10(halogal_tng[cents_tng]["M200"].values),
        np.log10(halogal_tng[cents_tng]["Mstar Subfind"].values),
        bins=bins,
        cmap=cmap,
        norm=norm,
        density=True,
    )
    tng_hist_raw_counts = np.histogram2d(
        np.log10(halogal_tng[cents_tng]["M200"].values),
        np.log10(halogal_tng[cents_tng]["Mstar Subfind"].values),
        bins=bins,
        density=False,
    )
    suff_counts_tng = np.sum(tng_hist_raw_counts[0], axis=0) > 0
    median_mstar_tng = bin_medians(
        np.log10(halogal_tng[cents_tng]["Mstar Subfind"]),
        np.log10(halogal_tng[cents_tng]["M200"]),
        mhalo_bins,
    )
    axes[2].plot(bin_mids[suff_counts_tng], median_mstar_tng[suff_counts_tng], ls="solid", color="#ffb700")
    magneticum_hist = axes[3].hist2d(
        np.log10(halogal_magneticum[cents_magneticum]["M200"].values),
        np.log10(halogal_magneticum[cents_magneticum]["Mstar Subfind"].values),
        bins=bins,
        cmap=cmap,
        norm=norm,
        density=True,
    )
    magneticum_hist_raw_counts = np.histogram2d(
        np.log10(halogal_magneticum[cents_magneticum]["M200"].values),
        np.log10(halogal_magneticum[cents_magneticum]["Mstar Subfind"].values),
        bins=bins,
        density=False,
    )
    suff_counts_magneticum = np.sum(magneticum_hist_raw_counts[0], axis=0) > 0
    median_mstar_magneticum = bin_medians(
        np.log10(halogal_magneticum[cents_magneticum]["Mstar Subfind"]),
        np.log10(halogal_magneticum[cents_magneticum]["M200"]),
        mhalo_bins,
    )
    axes[3].plot(
        bin_mids[suff_counts_magneticum],
        median_mstar_magneticum[suff_counts_magneticum],
        ls="solid",
        color="#ffb700",
    )
    fig.subplots_adjust(right=0.95)
    cbar_ax = fig.add_axes([0.96, 0.109, 0.01, 0.77])
    cbar = fig.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap=cmap), cax=cbar_ax, extend="max", fraction=0.05)
    counts_sims = [
        np.sum(nh_hist_raw_counts[0]),
        np.sum(eagle_hist_raw_counts[0]),
        np.sum(tng_hist_raw_counts[0]),
        np.sum(magneticum_hist_raw_counts[0]),
    ]
    for i, ax in enumerate(axes):
        ax.text(12.8, 9.7, f"$N_{{\mathrm{{centrals}}}}={int(counts_sims[i])}$", fontsize=8)
    axes[0].set_xlim((10.3, 14.7))
    axes[0].set_ylim((9.5, 12.6))
    axes[0].set_title("NewHorizon", fontsize=12)
    axes[1].set_title("EAGLE", fontsize=12)
    axes[2].set_title("TNG", fontsize=12)
    axes[3].set_title("Magneticum", fontsize=12)
    # for a in axes:
    #     a.tick_params('both',labelsize=12)
    fig.supxlabel(r"log$_{10}(M_{\rm 200, crit}/$M$_{\odot})$", fontsize=12)
    fig.supylabel(r"log$_{10}(M_{\star}/$M$_{\odot})$", fontsize=12, x=0.05)

    cbar.set_label("Normalised counts", fontsize=12)

    fig.savefig("./figures/halo_mass_stellar_mass_relation_normalised_v5.pdf", bbox_inches="tight")
    plt.close("all")
