"""Настройка путей, чтобы pytest видел пакет num_series."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))