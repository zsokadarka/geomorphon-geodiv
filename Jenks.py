import pandas as pd
import jenkspy
from pathlib import Path

# ---- BEÁLLÍTÁSOK ----

input_folder = Path(r"C:\Users\kadar\Documents\.Szakdoga\Geodiv_elemzes\jav\cell")
output_folder = input_folder / "jenks_output"

# ---- JENKS KATEGÓRIÁK SZÁMÍTÁSÁRA ALKALMAZANDÓ OSZLOP ----
value_col = "_GEODIV"

n_classes = 5

output_folder.mkdir(exist_ok=True)


# ---- JENKS OSZTÁLYOZÓ FÜGGVÉNY ----

def add_jenks_class(df, value_col, n_classes=5):
    # numerikussá alakítás
    df[value_col] = pd.to_numeric(df[value_col], errors="coerce")

    values = df[value_col].dropna().tolist()

    if len(values) == 0:
        raise ValueError("Nincs érvényes numerikus érték az oszlopban.")

    if len(set(values)) < n_classes:
        raise ValueError("Kevesebb egyedi érték van, mint a kért kategóriák száma.")

    # Jenks határok számítása
    breaks = jenkspy.jenks_breaks(values, n_classes=n_classes)

    print("Jenks határok:", breaks)

    # kategória hozzárendelése
    def classify(value):
        if pd.isna(value):
            return pd.NA

        for i in range(1, len(breaks)):
            if value <= breaks[i]:
                return i

        return n_classes

    df["jenks_class"] = df[value_col].apply(classify)

    return df


# ---- FÁJLOK FELDOLGOZÁSA ----

xlsx_files = list(input_folder.glob("*.xlsx"))

if not xlsx_files:
    raise FileNotFoundError("Nem találtam .xlsx fájlokat a megadott mappában.")

for file in xlsx_files:
    print(f"\nFeldolgozás: {file.name}")

    df = pd.read_excel(file)

    if value_col not in df.columns:
        print(f"Kihagyva, mert nincs ilyen oszlop: {value_col}")
        continue

    df = add_jenks_class(df, value_col, n_classes)

    output_file = output_folder / f"jenks_{file.stem}.xlsx"
    df.to_excel(output_file, index=False)

    print(f"Mentve: {output_file}")

print("\nKész.")