import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
EXAMPLES_DIR = os.path.join(DATA_DIR, "examples")
RULES_DIR = os.path.join(DATA_DIR, "rules")
RESULTS_DIR = os.path.join(PROJECT_ROOT, "results")
GRAMMARS_DIR = os.path.join(PROJECT_ROOT, "grammars")
PROMPTS_PATH = os.path.join(DATA_DIR, "prompts.json")