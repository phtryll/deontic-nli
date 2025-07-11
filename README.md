# Deontic NLI

This project explores how NLI systems understand deontic (normative) language.

We first translate deontic logic formulas into natural language, and then feed them into an NLI system for evaluation under the classic "entailment", "contradiction", "neutral" classification task.

## Table of Contents

- [Deontic NLI](#deontic-nli)
  - [Table of Contents](#table-of-contents)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Project structure](#project-structure)

## Installation

To get started, clone the repository and install the required dependencies:

```bash
git clone https://github.com/phtryll/deontic-nli.git
cd deontic-nli
pip install -r requirements.txt
```

## Usage

Below are some examples of how to use the CLI tool:

```bash
# Show the CFG grammar
python cli.py --show-grammar

# Generate 10 examples with a simple CFG
python cli.py --generate-examples 10 cfg

# Generate 10 examples using a probabilistic CFG
python cli.py --generate-examples 10 pcfg

# Generate 20 lexical items (default count) and output to console
python cli.py --generate-lexical-pool

# Generate 50 lexical items and save to JSON
python cli.py --generate-lexical-pool 50 --save

# Generate 20 lexical rules (default count) and output to console
python cli.py --generate-rules

# Generate 30 lexical rules and save to JSON
python cli.py --generate-rules 30 --save

# Reset the lexical items pool
python cli.py --reset lexical_items

# Reset the lexical rules pool
python cli.py --reset lexical_rules
```

## Project structure

The current project structure:

```plaintext
deontic-nli/
├── data/                           ← JSON data files  
│   ├── lexical_items_pool.json     ← Lexical items pool  
│   └── lexical_rules_pool.json     ← Lexical rules pool  
├── resources/                      ← CFG grammars  
│   ├── axiom_obrm.py               ← Deontic rule of monotonicity (OB-RM)  
│   ├── free_choice.py              ← Free‐choice permission  
│   ├── model_prompts.py            ← Prompts for lexical item generation  
│   └── operators.py                ← Deontic operators  
├── source/                         ← Application source code  
│   ├── cfg_utils.py                ← CFG 'Rule' and 'Tree' classes, 'unify' and 'join' functions 
│   ├── cfg.py                      ← CFG, probabilistic CFG and feature-based CFG class  
│   ├── generate_utils.py           ← Helper functions to generate lexical items and format them into CFG rules  
│   └── generate.py                 ← Main examples/rules generation pipeline  
├── cli.py                          ← Command-line interface  
├── README.md                       ← Project overview & instructions  
└── requirements.txt                ← Python package dependencies  
```
