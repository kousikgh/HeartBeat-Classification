"""Central application configuration.

All paths are relative to the project root, so the application has no
machine-specific hard-coded paths.
"""

from __future__ import annotations

from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent


class Config:
    """Default Flask configuration for local development."""

    SECRET_KEY = "development-only-change-before-deployment"
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5 MB upload limit
    DATABASE = BASE_DIR / "instance" / "heartbeat.db"
    MODEL_DIR = BASE_DIR / "models"
    RESULTS_DIR = BASE_DIR / "results"
    RAW_DATA_DIR = BASE_DIR / "data" / "raw"
    PROCESSED_DATA_DIR = BASE_DIR / "data" / "processed"
    MODEL_VERSION = "baseline-record-aware-v1"
