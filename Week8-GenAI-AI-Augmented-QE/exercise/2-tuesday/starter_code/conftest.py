"""conftest.py - makes `shopfront` importable and adds the --cases option. Do not edit."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent / "tools"))


def pytest_addoption(parser):
    parser.addoption("--cases", default=None,
                     help="File holding Claude's format-locked JSON reply (Stage 3)")
