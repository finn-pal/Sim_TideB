import json

import numpy as np

# Data to be written
dictionary = {"name": "sathiyajith", "rollno": 56, "cgpa": 8.6, "phonenumber": "9976770500"}

kpc_cgs = 3.08567758e21
G_cgs = 6.67e-8
Mo_cgs = 1.99e33
umass_GizToGas = 1.0  # 1e9Mo
umass = 1.0  # * umass_GizToGas
udist = 1.0  # kpc
uvel = np.sqrt(G_cgs * umass * Mo_cgs / (udist * kpc_cgs)) / 1e5
# uvel = 207.402593435
udens = umass * Mo_cgs / (udist * kpc_cgs) ** 3.0
utime = np.sqrt(1.0 / (udens * G_cgs))
sec2myr = 60.0 * 60.0 * 24.0 * 365.0 * 1e6

dictionary = {
    "kpc_cgs": kpc_cgs,
    "G_cgs": G_cgs,
    "Mo_cgs": Mo_cgs,
    "umass_GizToGas": umass_GizToGas,  # 1e9Mo
    "umass": umass,  # * umass_GizToGas
    "udist": udist,  # kpc
    "uvel": uvel,
    "utime": utime,
    "sec2myr": sec2myr,
}

# Serializing json
json_object = json.dumps(dictionary, indent=4)

# Writing to sample.json
with open("simulation_details/sim_units.json", "w") as outfile:
    outfile.write(json_object)
