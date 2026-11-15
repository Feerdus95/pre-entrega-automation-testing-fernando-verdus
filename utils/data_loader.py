import json
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def load_json(filename: str):
    """Load a test data file from data/ (kept free of Selenium so API tests can reuse it)."""
    with open(DATA_DIR / filename, encoding="utf-8") as file:
        return json.load(file)
