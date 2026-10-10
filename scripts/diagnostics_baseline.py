"""Read the exact reviewed diagnostics baseline from Git, without /tmp dependencies."""
from pathlib import Path
import subprocess
ROOT = Path(__file__).resolve().parents[1]
BASELINE_COMMIT = "d557db5fdc52cc89e721df5644218017db7230e0"
def baseline_bytes(relative):
    return subprocess.check_output(["git", "show", f"{BASELINE_COMMIT}:{relative}"], cwd=ROOT)
