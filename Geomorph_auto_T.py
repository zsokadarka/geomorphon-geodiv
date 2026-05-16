#---- GEOMORPHONOK AUTOMATIKUS GENERÁLÁSA MEGADOTT PARAMÉTEREK ALAPJÁN MAGYARORSZÁG MINTATERÜLETRE
# Exported from ArcGIS Pro notebook

import os
import arcpy
from datetime import datetime

arcpy.env.addOutputsToMap = False
arcpy.env.overwriteOutput = True



flat_list = [0.1,0.5,1,2]
res_list = [1]
skip_list = [0,1,2,5]

search_list = [300] 

  
for i in search_list: 
    L = i
    for j in flat_list:
        t = j
        for k in res_list: 
            r = k
            for l in skip_list:
                s = l
                search = L
                flat = t
                res = r
                skip = s
                if skip==0:
                    if isinstance(flat, float): # if flat type not integer
                        flat_txt = str(flat).replace(".", "")
                        name = f"T_L{search}_t{flat_txt}_r{res}"
                    else:
                        name = f"T_L{search}_t{flat}_r{res}"
                else:
                    #    name = f"T_L{search}_t{flat}_r{res}"
                    if isinstance(flat, float): # if flat type not integer
                        flat_txt = str(flat).replace(".", "")
                        name = f"T_L{search}_t{flat_txt}_r{res}_s{skip}"
                    else:
                        name = f"T_L{search}_t{flat}_r{res}_s{skip}"
                print(name)

    #output paths
                out_dir=r"C:\Users\kadar\Documents\.Szakdoga\Geomorphon\T"
                out_lf= os.path.join(out_dir,"Landforms", name) + ".tif"
                out_gm= os.path.join(out_dir,"Geomorphons", name) + "_gm.tif"
                #print(out_lf)
                #print (out_gm)
                with arcpy.EnvManager(scratchWorkspace=r"C:\Users\kadar\Documents\.Szakdoga\Geomorphon\T\Landforms"):
                    gm = arcpy.sa.GeomorphonLandforms(
                        in_surface_raster=r"C:\Users\kadar\Documents\.Szakdoga\ArcGIS_szakdoga\Szakdoga.gdb\DTM_1m_EOV_AoI",
                        out_geomorphons_raster=out_gm,
                        angle_threshold=flat,
                        distance_units="CELLS",
                        search_distance=search,
                        skip_distance=skip,
                        z_unit="METER"
                    )
                    gm.save(out_lf)
                    #print(name + " generated")

                    #aprx = arcpy.mp.ArcGISProject("CURRENT")
                    #map_name = "Tihany_geom"
                    #m = aprx.listMaps(map_name)[0]
                    #m.addDataFromPath(out_lf).name = name
print("done")


