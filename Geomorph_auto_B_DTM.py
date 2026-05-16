# ---- KÜLÖNBÖZŐ DEMEK ÖSSZEHASONLÍTÁSA UGYANAZON PARAMÉTEREKKEL ----
# Exported from ArcGIS Pro notebook

import os
import arcpy

arcpy.env.addOutputsToMap = False
arcpy.env.overwriteOutput = True

# ---- GEOMORPHON ALGORITMUS FUTTATÁSÁHOZ HASZNÁLT PARAMÉTEREK ---

search_list = [25,50,100,200]
flat_list = [0.5,1]
res_list = [10]

#A KIPRÓBÁLANDÓ DSM2DTM PUGINNEL MÓDOSÍTOTT COPERNICUS DEMEK
DTM_list = [r"C:\Users\kadar\Documents\.Szakdoga\DEM\Copernicus\Balaton_DSMtoDTM_Copernicus_EOV_10.tif",
            r"C:\Users\kadar\Documents\.Szakdoga\DEM\Copernicus\Balaton_DSMtoDTM_Copernicus_EOV_20.tif",
            r"C:\Users\kadar\Documents\.Szakdoga\DEM\Copernicus\Balaton_DSMtoDTM_Copernicus_EOV_30.tif",
            r"C:\Users\kadar\Documents\.Szakdoga\DEM\Copernicus\Balaton_DSMtoDTM_Copernicus_EOV_40.tif",
            r"C:\Users\kadar\Documents\.Szakdoga\DEM\Copernicus\Balaton_DSMtoDTM_Copernicus_EOV_40_s05.tif",
            r"C:\Users\kadar\Documents\.Szakdoga\DEM\Copernicus\Balaton_DSMtoDTM_Copernicus_EOV_50.tif",
            r"C:\Users\kadar\Documents\.Szakdoga\DEM\Copernicus\Balaton_DSMtoDTM_Copernicus_EOV_60.tif",
            r"C:\Users\kadar\Documents\.Szakdoga\DEM\Copernicus\Balaton_DSMtoDTM_Copernicus_EOV_70.tif",
            r"C:\Users\kadar\Documents\.Szakdoga\DEM\Copernicus\Balaton_DSMtoDTM_Copernicus_EOV_100.tif"]

for d in DTM_list:
    dtm = d
    demcell = d[-6:-4]
    print (demcell)
    for i in search_list: 
        L = i
        for j in flat_list:
            t = j
            for k in res_list: 
                r = k 
                search = L
                flat = t
                res = r
                #setting the parameters
    #search = 25
    #flat = 1
    #res = 30
    #generating the name
                #if res == 0.5:
                   # name = f"T_L{search}_t{flat}_r05"
                #else:
                #    name = f"T_L{search}_t{flat}_r{res}"
                if isinstance(flat, float): # if flat type not integer
                    flat_txt = str(flat).replace(".", "")
                    name = f"B_L{search}_t{flat_txt}_r{res}_DTM{demcell}"
                #elif flat == 0.1:
                    #name = f"T_L{search}_t01_r{res}"
                else:
                    name = f"B_L{search}_t{flat}_r{res}_DTM{demcell}"
                print(name)
    
    #output paths
                out_dir=r"C:\Users\kadar\Documents\.Szakdoga\Geomorphon\B\DTM"
                out_lf= os.path.join(out_dir,"Landforms", name) + ".tif"
                out_gm= os.path.join(out_dir,"Geomorphons", name) + "_gm.tif"
                #print(out_lf)
                print (out_gm)
                #with arcpy.EnvManager(scratchWorkspace=r"C:\Users\kadar\Documents\.Szakdoga\Geomorphon\B\DTM\Landforms"):
                gm = arcpy.sa.GeomorphonLandforms(
                    in_surface_raster=dtm,
                    out_geomorphons_raster=out_gm,
                    angle_threshold=flat,
                    distance_units="CELLS",
                    search_distance=search,
                    skip_distance=None,
                    z_unit="METER"
                )
                gm.save(out_lf)
                    #print(name + " generated")
                    #print(datetime.now)
    
                    #aprx = arcpy.mp.ArcGISProject("CURRENT")
                    #map_name = "Tihany_geom"
                    #m = aprx.listMaps(map_name)[0]
                    #m.addDataFromPath(out_lf).name = name
print("done")






