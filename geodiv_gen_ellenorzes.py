from pathlib import Path
import re
import pandas as pd

# ---- VIZSGÁLANDÓ MAPPÁK ----

folders = [
    r"C:\Users\kadar\Documents\.Szakdoga\Geodiv_elemzes\Balaton\GdCalc",
    r"C:\Users\kadar\Documents\.Szakdoga\Geodiv_elemzes\Balaton\GdCalc\skip",
    r"C:\Users\kadar\Documents\.Szakdoga\Geodiv_elemzes\Balaton\GdCalc\MERIT",
    r"C:\Users\kadar\Documents\.Szakdoga\Geodiv_elemzes\Mo\GdCalc",
    r"C:\Users\kadar\Documents\.Szakdoga\Geodiv_elemzes\Mo\GdCalc\skip",
    r"C:\Users\kadar\Documents\.Szakdoga\Geodiv_elemzes\Tihany\GdCalc\T_60hex",
    r"C:\Users\kadar\Documents\.Szakdoga\Geodiv_elemzes\Tihany\GdCalc\T_60hex\skip",
    r"C:\Users\kadar\Documents\.Szakdoga\Geodiv_elemzes\Tihany\GdCalc_10m",
]

# ---- EREDMÉNYEK ----

results = []


# ---- SEGÉDFÜGGVÉNY: L-PARAMÉTERTŐL KEZDŐDŐ RÉSZ KINYERÉSE ----

def get_param_part(name):
    """
    Kinyeri a névből az L-paramétertől kezdődő részt.
    Példa:
    Mo_L5_t01_r90_s1_geomorphon_grid.gpkg -> L5_t01_r90_s1
    B_1880_L5_t01_r90_s1 -> L5_t01_r90_s1
    """

    # levágjuk a fájlvégi fix részt, ha van
    name = name.replace("_geomorphon_grid.gpkg", "")

    # L-től kezdődő paraméterrész keresése
    match = re.search(r"L\d+_t\d+_r\d+(?:_s\d+)?", name)

    if match:
        return match.group(0)
    else:
        return None


# ---- FÁJLOK ELLENŐRZÉSE ----

for folder in folders:
    folder_path = Path(folder)

    if not folder_path.exists():
        print(f"Nem létezik, kihagyva: {folder_path}")
        continue

    # rekurzívan megkeresi az összes *_geomorphon_grid.gpkg fájlt
    gpkg_files = list(folder_path.rglob("*_geomorphon_grid.gpkg"))

    if not gpkg_files:
        print(f"Nincs geomorphon_grid.gpkg fájl itt: {folder_path}")
        continue

    for file in gpkg_files:
        subfolder_name = file.parent.name
        file_name = file.name

        folder_param = get_param_part(subfolder_name)
        file_param = get_param_part(file_name)

        if folder_param is None or file_param is None:
            status = "NEM KIOLVASHATÓ"
            match = False
        elif folder_param == file_param:
            status = "OK"
            match = True
        else:
            status = "ELTÉRÉS"
            match = False

        results.append({
            "main_folder": str(folder_path),
            "subfolder": subfolder_name,
            "file_name": file_name,
            "folder_param": folder_param,
            "file_param": file_param,
            "match": match,
            "status": status,
            "full_path": str(file)
        })


# ---- EREDMÉNY TÁBLÁZAT ----

result_df = pd.DataFrame(results)

if result_df.empty:
    print("Nem találtam ellenőrizhető fájlokat.")
else:
    print("\nEllenőrzés kész.")
    print(result_df[["subfolder", "file_name", "folder_param", "file_param", "status"]])

    # mentés Excelbe
    output_file = Path(r"C:\Users\kadar\Documents\.Szakdoga\Geodiv_elemzes\geomorphon_grid_nevellenorzes.xlsx")
    result_df.to_excel(output_file, index=False)

    print(f"\nEredmény mentve ide:")
    print(output_file)