import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
EXAMPLES_DIR = DATA_DIR / "examples"
RULES_DIR = DATA_DIR / "rules"
RESULTS_DIR = PROJECT_ROOT / "results"
GRAMMARS_DIR = PROJECT_ROOT / "grammars"
PROMPTS_PATH = DATA_DIR / "prompts.json"