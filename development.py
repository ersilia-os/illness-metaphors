import os
import shutil

results_dir = "results/pngs/with_reference/trachoma"

for fn in os.listdir(results_dir):
    if not fn.endswith(".png"):
        continue
    fs = fn.split("-")
    gn = "-".join([fs[0], fs[2], fs[1]] + fs[3:])
    shutil.move(os.path.join(results_dir, fn), os.path.join(results_dir, gn))