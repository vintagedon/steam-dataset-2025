#!/usr/bin/env python3
# =================================================================================================
# File:          setup-gpu01.py
# Project:       Steam Dataset 2025
# Repository:    https://github.com/vintagedon/steam-dataset-2025
# Author:        Don (vintagedon)  |  GitHub: https://github.com/vintagedon  |  ORCID: 0009-0008-7695-4093
# License:       MIT
# Last Updated:  2025-09-29
#
# Purpose:
#   Bootstrap a Python virtual environment with CUDA-enabled PyTorch and ML dependencies on Ubuntu
#   24.04, then verify GPU availability using a small NVML + torch probe.
#
# Section Map:
#   1) Docstring (original notes)  2) run_command helper  3) main() steps  4) __main__ guard
#
# Security:
#   - No secrets handled. Commands run under current user’s privileges.
#
# Change Log (docs-only):
#   - 2025-09-29  Added standardized header + inline comments; no behavior changes.
# =================================================================================================

"""
GPU ML Environment Setup - proj-gpu01
Python version for Ubuntu 24.04 with externally-managed-environment
"""

# --- Imports --------------------------------------------------------------------------------------
# Human: subprocess for shelling out; Path for FS ops; keep prints actionable on failures.
# ML:    DEPENDS_ON = ["python3-venv", "pip", "CUDA-enabled torch index (cu118)"]
import subprocess
import sys
import os
from pathlib import Path

# --- Core Component -------------------------------------------------------------------------------
# Human: small wrapper to run commands (optionally without shell) and surface stdout/stderr.
# ML:    CONTRACT: run_command(cmd, description, use_shell) -> bool
def run_command(cmd, description=None, use_shell=True):
    """Run a command and handle errors"""
    if description:
        print(f"Running: {description}")

    try:
        # The 'cmd' is now expected to be a list of arguments if use_shell is False
        result = subprocess.run(cmd, shell=use_shell, check=True, capture_output=True, text=True)
        if result.stdout.strip():
            print(result.stdout.strip())
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {cmd}")
        print(f"Error: {e}")
        if e.stderr:
            print(f"stderr: {e.stderr.strip()}")
        return False

# --- Orchestration -------------------------------------------------------------------------------
# Human: create venv, install package groups, set a bash alias, run a minimal GPU smoke test.
# ML:    ENTRYPOINT(main): idempotent where possible; safe to rerun if packages exist.
def main():
    print("Setting up Steam Dataset ML environment with CUDA on proj-gpu01...")

    # Define venv path
    venv_path = Path.home() / "venv" / "steam-ml"
    
    # Create parent directory if it doesn't exist
    venv_path.parent.mkdir(parents=True, exist_ok=True)

    # Create a fresh virtual environment
    if not venv_path.exists():
        print(f"Creating virtual environment at {venv_path}...")
        if not run_command(f"python3 -m venv {venv_path}", "Creating venv"):
            print("ERROR: Could not create virtual environment")
            sys.exit(1)

    pip_path = venv_path / "bin" / "pip"
    python_path = venv_path / "bin" / "python"

    if not pip_path.exists():
        print("ERROR: pip not found in virtual environment")
        sys.exit(1)

    print("Virtual environment is ready.")

    # Human: install in groups for clearer logs; cu118 wheel URL pins a CUDA build.
    packages = [
        "pip setuptools wheel",
        "numpy pandas scipy",
        "scikit-learn umap-learn",
        "psycopg2-binary",
        "matplotlib plotly",
        "torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118",
        "sentence-transformers",
        "tqdm",
        "python-dotenv",
        "psutil",
        "nvidia-ml-py"
    ]

    for package_group in packages:
        if not run_command(f"{pip_path} install --upgrade {package_group}", f"Installing {package_group}"):
            print(f"Warning: Failed to install {package_group}")

    # Add alias to bashrc
    bashrc_path = Path.home() / ".bashrc"
    alias_line = f"alias steam-ml='source {venv_path}/bin/activate'"
    try:
        if 'steam-ml' not in open(bashrc_path).read():
            with open(bashrc_path, 'a') as f:
                f.write(f"\n{alias_line}\n")
            print("Added steam-ml alias to .bashrc. Please run 'source ~/.bashrc' or restart your terminal.")
        else:
            print("steam-ml alias already exists in .bashrc")
    except FileNotFoundError:
        print(f"Warning: .bashrc not found. Could not add alias.")

    # --- CORRECTED GPU TEST -----------------------------------------------------------------------
    # Human: write a tiny Python script that checks torch + NVML without relying on shell quoting intricacies.
    print("\n--- Testing GPU Availability ---")
    gpu_test_script_content = '''
import torch
import nvidia_ml
try:
    nvidia_ml.nvmlInit()
    handle = nvidia_ml.nvmlDeviceGetHandleByIndex(0)
    print(f"CUDA Available: {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        print(f"GPU Device: {torch.cuda.get_device_name(0)}")
        print(f"CUDA Version: {torch.version.cuda}")
        print(f"Driver Version: {nvidia_ml.nvmlSystemGetDriverVersion()}")
    nvidia_ml.nvmlShutdown()
except Exception as e:
    print(f"Could not get GPU info: {e}")
    print("WARNING: CUDA might not be available to PyTorch.")
'''
    # Write the script to a temporary file
    gpu_test_file = Path("/tmp/gpu_test.py")
    with open(gpu_test_file, 'w') as f:
        f.write(gpu_test_script_content)

    # Execute the temporary file directly, avoiding the shell
    run_command([str(python_path), str(gpu_test_file)], description="Running GPU test script", use_shell=False)
    
    # Clean up the temporary file
    gpu_test_file.unlink()

    print("\nSteam Dataset ML environment setup complete!")
    print(f"Use '{'steam-ml'}' alias or run 'source {venv_path}/bin/activate' to activate.")

# --- Entry Point ---------------------------------------------------------------------------------
if __name__ == "__main__":
    main()
