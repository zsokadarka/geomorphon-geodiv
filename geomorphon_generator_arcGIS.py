


import arcpy
from pathlib import Path

search_input = arcpy.GetParameterAsText(0)
flat_input = arcpy.GetParameterAsText(1)
res_input = arcpy.GetParameterAsText(2)
skip_input = arcpy.GetParameterAsText(3)
dtm_input = arcpy.GetParameterAsText(4)
out_dir = Path(arcpy.GetParameterAsText(5))
name_prefix = arcpy.GetParameterAsText(6)



search_list = []
flat_list = []
res_list = []
skip_list = []
dtm_list = []

def parameter_input():
    search_list_text = search_input.split(",")

    for i in search_list_text:
        search_list.append(int(i))

    flat_list_text = flat_input.split(",")
    for i in flat_list_text:
        flat_list.append(float(i))

    res_list_text = res_input.split(",")
    for i in res_list_text:
        res_list.append(int(i))

    skip_list_text = skip_input.split(",")
    for i in skip_list_text:
        skip_list.append(int(i))
    return None

parameter_input()
arcpy.AddMessage(f"Search list = {search_list}")
arcpy.AddMessage(f"Flat list = {flat_list}")
arcpy.AddMessage(f"Used resolutions list = {res_list}")
arcpy.AddMessage(f"Used skip values list = {skip_list}")

# DEM INPUTS ------------------------------
dtm_list_text = dtm_input.split(",")
for dem in dtm_list_text:
    cleaned_path = dem.strip() # remove any space before or behind
    path_object = Path(cleaned_path)
    dtm_list.append(path_object)
arcpy.AddMessage(f"DEM list = {dtm_list}")

# -- GEOMORPHON GENERATOR LOOP ---------------------------
for d in dtm_list:
    dtm = d
    for i in search_list:
        look = i
        for j in flat_list:
            t = j
            for k in res_list:
                r = k
                for l in skip_list:
                    s = l
                    search = look
                    flat = t
                    res = r
                    skip = s

            # --- NAME SYNTAX ---------------------------------------------
                    if skip == 0:
                        if isinstance(flat, float):  # if flat type not integer
                            flat_txt = str(flat).replace(".", "")
                            name = f"{name_prefix}_L{search}_t{flat_txt}_r{res}"
                        else:
                            name = f"{name_prefix}_L{search}_t{flat}_r{res}"
                    else:
                        if isinstance(flat, float):  # if flat type not integer
                            flat_txt = str(flat).replace(".", "")
                            name = f"{name_prefix}_L{search}_t{flat_txt}_s{skip}_r{res}"
                        else:
                            name = f"{name_prefix}_L{search}_t{flat}_s{skip}_r{res}"
                    arcpy.AddMessage(name)

            #---OUTPUT PATHS -------
                    out_dir_lf = out_dir / "Landforms"
                    out_dir_lf.mkdir(parents=True, exist_ok=True)
                    out_dir_gm = out_dir / "Geomorphons"
                    out_dir_gm.mkdir(parents=True, exist_ok=True)
                    out_lf = out_dir_lf / f"{name}.tif"
                    out_gm = out_dir_gm / f"{name}_gm.tif"

                    #print(out_lf)
                    #print (out_gm)

            #---ARCGIS GEOMORPHON TOOL ------------

                    with arcpy.EnvManager(scratchWorkspace=str(out_dir_lf)):
                        gm = arcpy.sa.GeomorphonLandforms(
                            in_surface_raster=str(dtm),
                            out_geomorphons_raster=str(out_gm),
                            angle_threshold=flat,
                            distance_units="CELLS",
                            search_distance=search,
                            skip_distance=skip,
                            z_unit="METER"
                        )
                        gm.save(str(out_lf))
                        arcpy.AddMessage(name + " generated")


arcpy.AddMessage("Done")




