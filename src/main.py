import json
import time

from plotting import make_gif, migration_gif, migration_gif_comb

start = time.time()

# make_gif(init_time=10, timestep=10, num_timestep=99, gif_name="TideB_gc2.gif")

with open("gc_list.json") as json_file:
    gc_list = json.load(json_file)

iteration = gc_list["iteration2"]

# migration_gif(
#     init_time=10, timestep=10, num_timestep=99, iteration=iteration, gif_name="TideB_Migration2.gif"
# )

migration_gif_comb(
    init_time=10, timestep=10, num_timestep=99, gc_list=gc_list, gif_name="TideB_MigrationComb.gif"
)

end = time.time()
print("Runtime " + str(round(end - start, 2)) + " seconds")
