# ---- PARAMÉTEREK KIÍRATÁSA RÉTEGENKÉNT EXCELBEN ----
import pandas as pd

# fájl
file = r"C:\Users\kadar\Documents\.Szakdoga\Geodiv_elemzes\jav\retegstat_ossz_jav.xlsx"

df = pd.read_excel(file)

# --- PARAMÉTEREK KINYERÉSE ---
def parse_value(s):
    # levágjuk az első karaktert (pl. L, t, r, s)
    val = s[1:]

    # ha nincs vezető nulla → sima egész szám
    if not val.startswith("0"):
        return float(val)

    # ha van vezető nulla → tizedes érték
    return int(val) / (10 ** (len(val) - 1))
def extract_params(nev):
    parts = nev.split("_")

    L = 0
    t = 0
    r = 0
    s = 0

    for p in parts:
        if p.startswith("L"):
            L = parse_value(p)
        elif p.startswith("t"):
            t = parse_value(p)
        elif p.startswith("r"):
            r = parse_value(p)
        elif p.startswith("s"):
            s = parse_value(p)

    return pd.Series([L, t, r, s])


# új oszlopok létrehozása
df[["L", "t", "r", "s"]] = df["nev"].apply(extract_params)

# mentés
df.to_excel(file, index=False)

print("Kész.")