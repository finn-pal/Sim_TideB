from enum import Enum

import numpy as np


class ParticleType(Enum):
    stars = "stars"
    gas = "gas"
    dm = "dm"
    all = ""


class Part_Select(Enum):
    get_all = "get_all"
    get_rng = "get_rng"
    exc_rng = "exc_rng"
    get_one = "get_one"
    get_lst = "get_lst"


def filter_particles(
    s,
    part_type: ParticleType = "stars",
    part_select: Part_Select = "get_all",
    rng_min: int = 1008463671,
    rng_max: int = 1008473670,
    part_id: int = 1008464975,
    par_lst: list = [],
):
    # type assertion
    if part_type not in ParticleType:
        raise ValueError("%r is not valid; possible choices: %r" % (part_type, list(ParticleType)))

    if part_type == "stars":
        h = s.s
    elif part_type == "gas":
        h = s.g
    elif part_type == "gas":
        h = s.g
    elif part_select == "all":
        h = s

    # type assertion
    if part_select not in Part_Select:
        raise ValueError("%r is not valid; possible choices: %r" % (part_select, list(Part_Select)))

    if part_select == "get_all":
        h = h
    elif part_select == "get_rng":
        h = h[(h["iord"] >= rng_min) & (h["iord"] <= rng_max)]
    elif part_select == "exc_rng":
        h = h[(h["iord"] < rng_min) | (h["iord"] > rng_max)]
    elif part_select == "get_one":
        h = h[(h["iord"] == part_id)]
    elif part_select == "get_lst":
        mask = np.isin(h["iord"], par_lst)
        h = h[mask]

    return h


def get_pos(s) -> dict:
    iord = [iod for iod in s["iord"]]
    x = [xi for xi in s["x"]]
    y = [yi for yi in s["y"]]
    z = [zi for zi in s["z"]]
    r = [ri for ri in s["r"]]

    pos_dict = {"iord": iord, "x": x, "y": y, "z": z, "r": r}

    return pos_dict


def get_vel(s) -> dict:
    iord = [iod for iod in s["iord"]]
    vx = [vxi for vxi in s["vx"]]
    vy = [vyi for vyi in s["vy"]]
    vz = [vzi for vzi in s["vz"]]

    vel_dict = {"iord": iord, "vx": vx, "vy": vy, "vz": vz}

    return vel_dict


def get_kinematics(s) -> dict:
    pos = get_pos(s)
    vel = get_vel(s)

    # km **2 / s ** 2
    e_pot = [phi for phi in s["phi"]]
    # e_kin = [0.5 * (vxi**2 + vyi**2 + vzi**2) for vxi, vyi, vzi in zip(vel["vx"], vel["vy"], vel["vz"])]
    # e_tot = [e_kini + e_poti for e_kini, e_poti in zip(e_kin, e_pot)]
    e_kin = [ke for ke in s["ke"]]
    e_tot = [te for te in s["te"]]

    # kpc km / s
    # lz = [rxi * vyi - ryi * vxi for rxi, ryi, vxi, vyi in zip(pos["x"], pos["y"], vel["vx"], vel["vy"])]
    lz = [jz for jz in s["jz"]]

    kin_dict = {
        "iord": pos["iord"],
        "x": pos["x"],
        "y": pos["y"],
        "z": pos["z"],
        "r": pos["r"],
        "vx": vel["vx"],
        "vy": vel["vy"],
        "vz": vel["vy"],
        "e_pot": e_pot,
        "e_kin": e_kin,
        "e_tot": e_tot,
        "lz": lz,
    }

    return kin_dict
