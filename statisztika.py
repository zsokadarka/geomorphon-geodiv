# ---- SPEARMAN ÉS PEARSON KORRELÁCIÓ SZÁMÍTÁSA GEOMORFODIVERRZITÁS RÉTEGEKRE ----
import pandas as pd
from pathlib import Path

reteg_mappa = Path(r"C:\Users\kadar\Documents\.Szakdoga\Geodiv_elemzes\jav")
cella_mappa = Path(r"C:\Users\kadar\Documents\.Szakdoga\Geodiv_elemzes\jav\cell")
reteg_mappa.mkdir(exist_ok=True)
cella_mappa.mkdir(exist_ok=True)

eredmenyek = []

for reteg_file in reteg_mappa.glob("retegstat_*.xlsx"):

    # név kinyerése: retegstat_B_1880... -> B_1880...
    nev = reteg_file.stem.replace("retegstat_", "")

    # megfelelő cellastat fájl
    cella_file = cella_mappa / f"cellstat_{nev}.xlsx"

    # rétegstat beolvasása
    reteg_df = pd.read_excel(reteg_file)

    # legyen benne a név is
    reteg_df["nev"] = nev

    # cellastat beolvasása
    cella_df = pd.read_excel(cella_file)

    # Pearson és Spearman
    pearson = cella_df["_GEODIV"].corr(cella_df["ref_GEODIV"], method="pearson")
    spearman = cella_df["_GEODIV"].corr(cella_df["ref_GEODIV"], method="spearman")

    # új oszlopok hozzáadása
    reteg_df["pearson_GEODIV"] = pearson
    reteg_df["spearman_GEODIV"] = spearman

    eredmenyek.append(reteg_df)

## összes rétegstat egyesítése
ossz = pd.concat(eredmenyek, ignore_index=True)

# mentés
ossz.to_excel(reteg_mappa / "retegstat_ossz_jav.xlsx", index=False)

print("Kész.")