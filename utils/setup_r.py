# setup_r_env.py
import subprocess
import os
import sys

RENV_LOCK = "renv.lock"
RENV_LIBRARY = "renv/library"

def check_r_installed():
    """Check that R is installed and accessible."""
    try:
        result = subprocess.run(
            ["Rscript", "--version"],
            capture_output=True,
            text=True
        )
        print(f"R found: {result.stdout.strip()}")
        return True
    except FileNotFoundError:
        print("ERROR: R is not installed or not on PATH.")
        return False

def renv_is_setup():
    """Check if renv library already exists."""
    return os.path.exists(RENV_LIBRARY)

def setup_renv():
    """Restore renv from lockfile."""
    print("Setting up R environment from renv.lock...")
    result = subprocess.run(
        ["Rscript", "-e", 
         f'renv::restore(project = ".", lockfile = "{RENV_LOCK}")'],
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        print(f"ERROR setting up R environment:\n{result.stderr}")
        sys.exit(1)
    else:
        print("R environment set up successfully!")

def run_setup():
    if not check_r_installed():
        sys.exit(1)

    if renv_is_setup():
        print("R environment already set up, skipping.")
    else:
        setup_renv()
