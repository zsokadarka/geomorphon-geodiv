import os
# ---- MAPPÁK LÉTREHOZÁSA A MEGFELELŐ NEVEKKEL
base_path = r"C:\Users\kadar\Documents\.Szakdoga\Geodiv_elemzes\Tihany\GdCalc_10m"

data = """
T_60_L10_t01_r10_s1
T_60_L10_t01_r10_s2
T_60_L10_t01_r10_s5
T_60_L10_t05_r10_s1
T_60_L10_t05_r10_s2
T_60_L10_t05_r10_s5
T_60_L10_t1_r10_s1
T_60_L10_t1_r10_s2
T_60_L10_t1_r10_s5
T_60_L10_t2_r10_s1
T_60_L10_t2_r10_s2
T_60_L10_t2_r10_s5

"""

# sorokra bontás
folders = data.strip().split("\n")

for f in folders:
    folder_path = os.path.join(base_path, f.strip())
    os.makedirs(folder_path, exist_ok=True)

print("Kész")