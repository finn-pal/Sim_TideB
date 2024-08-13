import json

from data_pull import data_pull
from kinematics import filter_particles
from plotting import migration_plot

init_time = 10
updt_time = 100

with open("gc_list.json") as json_file:
    gc_list = json.load(json_file)

iteration = gc_list["iteration1"]

s_init = data_pull(init_time)
s_updt = data_pull(updt_time)

s_init = filter_particles(s_init, part_type="stars", part_select="get_lst", par_lst=iteration)
s_updt = filter_particles(s_updt, part_type="stars", part_select="get_lst", par_lst=iteration)

migration_plot(s_init, s_updt)
