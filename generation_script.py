"""Script to generate synthetic data for lag-lock uncertainty analysis."""
import sys
from pathlib import Path
import pandas as pd

SCRIPTS_DIR = Path(__file__).resolve().parents[1] / 'scripts'
sys.path.insert(0, str(SCRIPTS_DIR))

from phase2_upgrade_selected import generate_data  # noqa: E402

df = generate_data('lag-lock-uncertainty', 20260306)
output = Path(__file__).resolve().parent / 'lag_lock_uncertainty_dataset.csv'
df.to_csv(output, index=False)
print('Generated', output.name, 'with', len(df), 'rows')
