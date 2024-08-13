import math
import random

import matplotlib.pyplot as plt
import numpy as np
from data_pull import data_pull
from kinematics import filter_particles


def gc_const(
    s,
    num_gc_0: int = 7,
    num_gc_1: int = 3,
    num_gc_2: int = 3,
    min0: float = 0.9,
    max0: float = 1.9,
    min1: float = None,
    max1: float = 4.75,
    min2: float = None,
    max2: float = 10,
):
    if min1 is None:
        min1 = max0
    if min2 is None:
        min2 = max1

    PI = math.pi

    com_min = 1008463671
    com_max = 1008473670

    zlim = 2

    s_cen = filter_particles(s, part_type="stars", part_select="exc_rng", rng_min=com_min, rng_max=com_max)
    s_const = s_cen[(s_cen["mass"] > 1e4) & (s_cen["r"] < 10)]

    full_circ = 2 * math.pi  # deg
    div_circ = full_circ / num_gc_0

    part_0_ls = []
    i = 0

    s_ang = s_const[(s_const["az"] > i * div_circ - PI) & (s_const["az"] < (i + 1) * div_circ - PI)]
    s_ang_rad = s_ang[(s_ang["r"] > min0) & (s_ang["r"] < max0)]
    ang_rad_iord = s_ang_rad["iord"]

    while i < num_gc_0:
        iord_choice = random.choice(ang_rad_iord)
        part_0_ls.append(iord_choice)

        i += 1

    part_1_ls = []
    i = 0

    s_hei = s_const[(s_const["z"] > -zlim) & (s_const["z"] < zlim)]
    s_hei_rad = s_hei[(s_hei["r"] > min1) & (s_hei["r"] < max1)]
    hei_rad_iord = s_hei_rad["iord"]

    while i < num_gc_1:
        iord_choice = random.choice(hei_rad_iord)
        part_1_ls.append(iord_choice)

        i += 1

    part_2_ls = []
    i = 0

    s_hei = s_const[(s_const["z"] > -zlim) & (s_const["z"] < zlim)]
    s_hei_rad = s_hei[(s_hei["r"] > min2) & (s_hei["r"] < max2)]
    hei_rad_iord = s_hei_rad["iord"]

    while i < num_gc_2:
        iord_choice = random.choice(hei_rad_iord)
        part_2_ls.append(iord_choice)

        i += 1

    commplete_list = part_0_ls + part_1_ls + part_2_ls
    print(commplete_list)


init_time = 1

s = data_pull(init_time)
gc_const(s)
