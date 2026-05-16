# ---- GEOMORPHON NÉVLISTA GENERÁLÁSA PARAMÉTEREK ALAPJÁN ----
# Exported from ArcGIS Pro notebook

import os
import arcpy


arcpy.env.addOutputsToMap = False
arcpy.env.overwriteOutput = True



search_list = [5,10,25,50,100,200,300]
flat_list = [0.1,0.5,1,2,3]
res_list = [90]
skip_list = [1,2,5,7,10,15,20,25,50]

DTM_list = [r"C:\Users\kadar\Documents\.Szakdoga\DEM\MERIT DEM\Mo_DEM_MERIT_90m.tif"]
    #r"C:\Users\kadar\Documents\.Szakdoga\DEM\Copernicus\Balaton_DSMtoDTM_Copernicus_EOV_10.tif"]
#            r"C:\Users\kadar\Documents\.Szakdoga\DEM\Copernicus\Balaton_DSMtoDTM_Copernicus_EOV_20.tif",
#         r"C:\Users\kadar\Documents\.Szakdoga\DEM\Copernicus\Balaton_DSMtoDTM_Copernicus_EOV_30.tif",
#           r"C:\Users\kadar\Documents\.Szakdoga\DEM\Copernicus\Balaton_DSMtoDTM_Copernicus_EOV_40.tif",
#            r"C:\Users\kadar\Documents\.Szakdoga\DEM\Copernicus\Balaton_DSMtoDTM_Copernicus_EOV_40_s05.tif",
 #           r"C:\Users\kadar\Documents\.Szakdoga\DEM\Copernicus\Balaton_DSMtoDTM_Copernicus_EOV_50.tif",
 #           r"C:\Users\kadar\Documents\.Szakdoga\DEM\Copernicus\Balaton_DSMtoDTM_Copernicus_EOV_60.tif",
 #           r"C:\Users\kadar\Documents\.Szakdoga\DEM\Copernicus\Balaton_DSMtoDTM_Copernicus_EOV_70.tif",
 #           r"C:\Users\kadar\Documents\.Szakdoga\DEM\Copernicus\Balaton_DSMtoDTM_Copernicus_EOV_100.tif"]
            
for d in DTM_list:
    dtm = d
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
                            name = f"B_1880_L{search}_t{flat_txt}_r{res}"
                        else:
                            name = f"B_1880_L{search}_t{flat}_r{res}"
                    else:
                        if isinstance(flat, float): # if flat type not integer
                            flat_txt = str(flat).replace(".", "")
                            name = f"B_1880_L{search}_t{flat_txt}_r{res}_s{skip}"
                        else:
                            name = f"B_1880_L{search}_t{flat}_r{res}_s{skip}"

                    print(name)

print("done")






