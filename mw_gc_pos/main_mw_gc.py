from astropy.table import Table
from func_mw.mw_gc_pos import mw_gc_pos

data_table = Table.read("mw_gc_pos/d_imp_mw/orbit_details.csv")

mw_gc_pos(data_table)
