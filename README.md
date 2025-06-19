# Deontic NLI

This project explores how NLI systems understand deontic (normative) language.

We first translate deontic logic formulas into natural language, and then feed them into an NLI system for evaluation.

## Project Structure

- **source/cfg.py**: Implements the `CFG` class which manages context-free grammar rules, identifies terminals and non-terminals, maps rules, and generates random parse trees. Includes methods for representing the grammar and printing trees.

- **source/utils.py**: Provides helper classes and functions:
  - `Rule`: Represents a grammar production with a left non-terminal and a list of right-hand symbols.
  - `Tree`: Represents parse trees, with methods to output the terminal sequence and to render the tree in bracketed notation.
  - `join(tokens)`: Utility function to format a list of tokens into a readable string.

- **resources/operators_formal.py**: Defines `operators_formal`, a set of `Rule` instances using formal logical symbols (`↔`, `→`, `∧`, `∨`) and modal operator abbreviations (`PE`, `OB`, `FO`, `OP`, `OM`, `NO`) along with atomic arguments (`p`, `q`, `¬p`, `¬q`) for parsing and generating deontic logic formulas.

- **resources/operators_natural.py**: Defines `operators_natural`, a set of `Rule` instances using natural-language modal operators (e.g., "il est permis que", "il est obligatoire que") and atomic arguments (`p`, `q`, `non p`, `non q`) for parsing and generating deontic logic sentences in French.
- **testing.py**: A script that initializes the `CFG` with `operators_natural`, generates random examples, joins tokens into sentences, and prints the results to demonstrate the grammar in action.

## Usage

1. Define or modify grammar rules in the `resources` directory (e.g., `operators_formal.py`).
2. Use `source/cfg.py` to load these rules and generate random sentences or parse trees.
3. Convert generated token lists into strings using `source/utils.py`'s `join` function for downstream processing.
