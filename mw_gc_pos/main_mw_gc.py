from astropy.table import Table
from func_mw.mw_gc_cyl import mw_gc_vel
from func_mw.mw_gc_iom import plot_iom
from func_mw.mw_gc_pos import mw_gc_pos

data_table = Table.read("mw_gc_pos/d_imp_mw/orbit_details.csv")
circular_table = Table.read("mw_gc_pos/d_imp_mw/circular_orbit.csv")

mw_gc_pos(data_table, plot_show=False, plot_save=True)
mw_gc_vel(data_table, sigma_z_thick=41.45, plot_show=False, plot_save=True)

plot_iom(data_table, circular_table, False, True)
