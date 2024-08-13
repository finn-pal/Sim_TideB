import numpy as np


def com_star_pos(snapshot, com_id_min: int = 1008463671, com_id_max: int = 1008473670) -> dict:
    t_now = snapshot.properties["time"].in_units("Myr")
    timestr = str(np.round(float(t_now), 1))

    star = snapshot.stars

    com_id = [id for id in star["iord"] if id >= com_id_min and id <= com_id_max]
    com_x = [ps[0] for ps, id in zip(star["pos"], star["iord"]) if id >= com_id_min and id <= com_id_max]
    com_y = [ps[1] for ps, id in zip(star["pos"], star["iord"]) if id >= com_id_min and id <= com_id_max]
    com_z = [ps[2] for ps, id in zip(star["pos"], star["iord"]) if id >= com_id_min and id <= com_id_max]

    com_pos_dict = {"time": timestr, "iord": com_id, "x": com_x, "y": com_y, "z": com_z}

    return com_pos_dict
