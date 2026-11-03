import qgis
import processing

from qgis.core import  (QgsProcessingAlgorithm,
    QgsProcessingParameterString,
    QgsProcessingParameterFolderDestination,
    QgsProcessingParameterFile,
    QgsProcessingParameterBoolean)

from pathlib import Path
import datetime
import time
import csv

class Geomorf_batch_gen(QgsProcessingAlgorithm):
    def initAlgorithm(self, config=None):

        # DEFINING PARAMETERS
        self.addParameter(
            QgsProcessingParameterString("search_input", "Search values separated by commas:", defaultValue="25"))

        self.addParameter(QgsProcessingParameterString("flat_input", "Flatness treshold values separated by commas:",
                                                       defaultValue="1"))

        self.addParameter(QgsProcessingParameterString("res_input", "Used DEM resolution in meters:", defaultValue="30"))

        self.addParameter(QgsProcessingParameterString("skip_input", "Skip values separated by commas:",
                                                       defaultValue="5"))

        self.addParameter(
            QgsProcessingParameterFile("dtm_input", "DTM path to use:", behavior=QgsProcessingParameterFile.File,
                                       fileFilter="Raster files (*.tif *.tiff *.img *.asc)"))

        self.addParameter(QgsProcessingParameterFolderDestination("out_dir", "Output directory path:"))

        self.addParameter(QgsProcessingParameterString("name_prefix", "Name prefix (study area):"))

        self.addParameter(QgsProcessingParameterBoolean("save2csv", "Save to CSV?", defaultValue=True))

    # MAIN TOOL
    def processAlgorithm(self, parameters, context, feedback):
        # DEFINING INPUT PARAMETERS AS VARIABLES
        search_input = self.parameterAsString(parameters, "search_input", context)

        flat_input = self.parameterAsString(parameters, "flat_input", context)

        res_input = self.parameterAsString(parameters, "res_input", context)

        skip_input = self.parameterAsString(parameters, "skip_input", context)

        dtm_input = self.parameterAsFile(parameters, "dtm_input", context)

        out_dir = Path(self.parameterAsString(parameters, "out_dir", context))

        name_prefix = self.parameterAsString(parameters, "name_prefix", context)

        save2csv = self.parameterAsBoolean(parameters, "save2csv", context)

        # CONVERTING STRING INPUT TO LISTS
        def parameter_input():
            search_list = []
            flat_list = []
            res_list = []
            skip_list = []
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

            feedback.pushInfo(f"Search list = {search_list}")
            feedback.pushInfo(f"Flat list = {flat_list}")
            feedback.pushInfo(f"Used resolutions list = {res_list}")
            feedback.pushInfo(f"Used skip values list = {skip_list}")
            feedback.pushInfo(f"Output folder path = {out_dir}")
            return search_list, flat_list, res_list, skip_list

        # CLEANING INPUT DEM PATH
        def dem_input():
            dtm_list = []
            for dem in dtm_input.split(","):
                cleaned_path = dem.strip()  # remove any space before or behind
                path_object = Path(cleaned_path)
                dtm_list.append(path_object)
            feedback.pushInfo(f"DEM list = {dtm_list}")
            return dtm_list

        # CREATING LOG
        def save_to_csv(csv_name):
            if save2csv:
                csv_file = out_dir / csv_name

                file_is_empty = not csv_file.exists() or csv_file.stat().st_size == 0  # check whether there is a file already

                with open(csv_file, "a", newline="", encoding="utf-8") as f:
                    writer = csv.writer(f, delimiter=",")

                    if file_is_empty:  # header if new file is needed
                        writer.writerow(
                            ["area", "name", "L", "s", "t", "res", "DEM_path", "output_path", "date", "elapsed_s"])
            return csv_file

        # CREATING NAMING CONVENTION
        def naming(search, skip, flat, res):

            if flat.is_integer():
                flat2 = int(flat)
                name = f"{name_prefix}_L{search}_t{flat2}_s{skip}_r{res}"
            else:
                flat2 = str(flat).replace(".", "")

                name = f"{name_prefix}_L{search}_t{flat2}_s{skip}_r{res}"
            return name

        # GENERATOR TOOL WITH ALL THE PARAMETER-COMBINATIONS
        def geomorph_generator(search_list, flat_list, res_list, skip_list, dtm_list, csv_file):
            gen_count = 0
            count = len(search_list) * len(flat_list) * len(skip_list)
            for dtm in dtm_list:
                for search in search_list:
                    for flat in flat_list:
                        for res in res_list:
                            for skip in skip_list:
                                name = naming(search, skip, flat, res)
                                if skip >= search:  # skip must be smaller than the lookup distance
                                    count -= 1
                                    feedback.pushInfo(
                                        f"ERROR: Skip value must be smaller than the lookup distance, {name} not generated.")
                                    continue

                                start_time = time.perf_counter()
                                now = datetime.datetime.now()
                                current_time = now.strftime("%H:%M:%S")
                                feedback.pushInfo(f"##{gen_count + 1}/{count}:  {name} started at {current_time}")

                                # output paths
                                out_dir_lf = out_dir / "Landforms"
                                out_dir_lf.mkdir(parents=True, exist_ok=True)
                                out_lf = out_dir_lf / f"{name}.tif"

                                # RUNNING GRASS R.GEOMORPHON TOOL IN PYQGIS
                                processing.run(
                                    "grass:r.geomorphon", {
                                        'elevation': str(dtm),
                                        'search': search, 'skip': skip, 'flat': flat, 'dist': 0,
                                        'forms': str(out_lf),
                                        '-m': False, '-e': False, 'GRASS_REGION_PARAMETER': None,
                                        'GRASS_REGION_CELLSIZE_PARAMETER': 0, 'GRASS_RASTER_FORMAT_OPT': '',
                                        'GRASS_RASTER_FORMAT_META': ''}, context=context, feedback=feedback)

                                end_time = time.perf_counter()
                                elapsed = end_time - start_time
                                now = datetime.datetime.now()
                                end_hour = now.strftime("%H:%M:%S")
                                gen_count += 1
                                feedback.pushInfo(
                                    f"##{gen_count}/{count}:  {name} generated in {elapsed:.2f} seconds, finished at {end_hour}.")
                                feedback.pushInfo("  ")
                                feedback.pushInfo("  ")

                                # ---WRITING CSV------------------

                                if save2csv:
                                    with open(csv_file, "a", newline="", encoding="utf-8") as f:
                                        writer = csv.writer(f, delimiter=",")
                                        writer.writerow(
                                            [name_prefix, name, search, skip, flat, res, str(dtm), str(out_lf),
                                             datetime.datetime.now(), round(elapsed, 2)])
            return gen_count

        # CALLING FUNCTIONS
        search_list, flat_list, res_list, skip_list = parameter_input()
        dtm_list = dem_input()
        csv_file = save_to_csv(f"geomorf_generalt.csv")
        gen_count = geomorph_generator(search_list, flat_list, res_list, skip_list, dtm_list, csv_file)

        # END INFO
        feedback.pushInfo("Done")
        feedback.pushInfo(f"{gen_count} files generated.")
        return {}

    def name(self):
        return "geomorphon_batch"

    def displayName(self):
        return "Geomorphon Batch"

    def createInstance(self):
        return Geomorf_batch_gen()
