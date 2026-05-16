import pandas as pd
from pathlib import Path

# ---- BEÁLLÍTÁSOK ----

input_folder = Path(r"C:\Users\kadar\Documents\.Szakdoga\Geodiv_elemzes\Balaton\Stat\Cella\jenks_output")

jenks_col = "jenks_class"

output_file = input_folder / "jenks_gyakorisag_B.xlsx"


# ---- FÁJLOK BEOLVASÁSA ----

all_data = []

for file in input_folder.glob("*.xlsx"):

    # Ideiglenes Excel fájlok kihagyása
    if file.name.startswith("~$"):
        continue

    # A saját output fájl kihagyása, ha újrafuttatod a programot
    if file.name == output_file.name:
        continue

    print(f"Beolvasás: {file.name}")

    try:
        df = pd.read_excel(file, engine="openpyxl")
    except Exception as e:
        print(f"Kihagyva, mert nem sikerült beolvasni: {file.name}")
        print(f"Hiba: {e}")
        continue

    cell_id_col = "fid"

    if jenks_col not in df.columns:
        print(f"Kihagyva, mert nincs ilyen oszlop: {jenks_col}")
        continue

    temp = df[[cell_id_col, jenks_col]].copy()
    temp = temp.rename(columns={cell_id_col: "cell_id"})

    all_data.append(temp)


# ---- ELLENŐRZÉS ----

if not all_data:
    raise ValueError("Nem sikerült egyetlen használható fájlt sem beolvasni.")


# ---- ÖSSZEFŰZÉS ----

all_df = pd.concat(all_data, ignore_index=True)


# ---- GYAKORISÁG SZÁMÍTÁSA ----

counts = pd.crosstab(all_df["cell_id"], all_df[jenks_col])

# biztosítjuk, hogy mind az 5 kategória oszlopa meglegyen
for i in range(1, 6):
    if i not in counts.columns:
        counts[i] = 0

counts = counts[[1, 2, 3, 4, 5]]

counts.columns = [
    "jenks_1_count",
    "jenks_2_count",
    "jenks_3_count",
    "jenks_4_count",
    "jenks_5_count"
]


# ---- SZÁZALÉK SZÁMÍTÁSA ----

total = counts.sum(axis=1)

percentages = counts.div(total, axis=0) * 100

percentages.columns = [
    "jenks_1_percent",
    "jenks_2_percent",
    "jenks_3_percent",
    "jenks_4_percent",
    "jenks_5_percent"
]


# ---- EREDMÉNY ÖSSZERAKÁSA ----

result = pd.concat([counts, percentages], axis=1)

result = result.reset_index()


# ---- MENTÉS ----

result.to_excel(output_file, index=False)

print("Kész.")
print(f"Eredmény mentve ide: {output_file}")