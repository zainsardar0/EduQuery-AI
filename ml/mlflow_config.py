"""
EduQuery AI — MLflow Configuration
====================================
Central MLflow setup for experiment tracking and model registry.
"""

import os
from pathlib import Path

import mlflow

PROJECT_ROOT = Path(__file__).resolve().parent.parent
MLRUNS_DIR = PROJECT_ROOT / "ml" / "mlruns"
REPORTS_DIR = PROJECT_ROOT / "ml" / "reports"


def setup_mlflow() -> None:
    """Configure MLflow tracking URI and create required directories."""
    MLRUNS_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    db_path = MLRUNS_DIR / "mlflow.db"
    tracking_uri = f"sqlite:///{db_path}"
    mlflow.set_tracking_uri(tracking_uri)

    print(f"  MLflow tracking URI: {tracking_uri}")
    print(f"  Reports directory:   {REPORTS_DIR}")


def get_or_create_experiment(name: str) -> str:
    """Get or create an MLflow experiment by name, return experiment ID."""
    experiment = mlflow.get_experiment_by_name(name)
    if experiment is None:
        experiment_id = mlflow.create_experiment(name)
    else:
        experiment_id = experiment.experiment_id
    return experiment_id
