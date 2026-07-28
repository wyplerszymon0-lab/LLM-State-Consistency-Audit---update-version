"""Discovers model submissions under models/ that expose a run() entry point."""

import importlib
import pkgutil
from pathlib import Path

MODELS_PACKAGE = "models"


def discover_models():
    """Return a list of (display_name, module) for every models/*.py submission."""
    models_dir = Path(__file__).resolve().parent.parent / "models"
    results = []
    for _finder, module_name, is_pkg in pkgutil.iter_modules([str(models_dir)]):
        if is_pkg or module_name.startswith("_"):
            continue
        module = importlib.import_module(f"{MODELS_PACKAGE}.{module_name}")
        if not hasattr(module, "run"):
            continue
        display_name = getattr(module, "MODEL_NAME", module_name)
        results.append((display_name, module))
    return results
