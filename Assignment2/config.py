import os
from pathlib import Path

DATASET_DIR = Path("./datasets")
PLOT_DIR = Path("./PLOT")

if not os.path.exists(DATASET_DIR):
    os.mkdir(DATASET_DIR)

if not os.path.exists(PLOT_DIR):
    os.mkdir(PLOT_DIR)

CONFIG = {
    "DATASET_DIR": DATASET_DIR,
    "PLOT_DIR": PLOT_DIR,
}