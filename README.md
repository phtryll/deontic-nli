# Deontic NLI

This project explores how NLI systems understand deontic (normative) language.

We first translate deontic logic formulas into natural language, and then feed them into an NLI system for evaluation.

## Current Progress

The TODO list for the project is currently:

- [x] Implement a simple CFG
- [x] Implement automatic CFG rules generation through a masked LLM
- [x] Simple grammar for deontic operator formulas
- [x] Simple grammar for free-choice disjunction formulas
- [x] Simple grammar for OB-RM axiom formulas
- [ ] Include rules to generate natural language examples from the formulas
- [ ] Improve the quality of automatic CFG rule generation
- [ ] Include many more grammars generating specific deontic expressions
- [ ] Implement `.json` exporting of examples
- [ ] Transform examples into premise-conclusion pairs
- [ ] Implement evaluation of pairs with a NLI model
- [ ] Evaluate different models, add benchmarks

## Project Structure

- `source/cfg.py`: Implements the `CFG` class which manages context-free grammar rules, identifies terminals and non-terminals, maps rules, and generates random parse trees. Includes methods for representing the grammar and printing trees.

- `source/cfg_utils.py`: Provides helper classes and functions:
  - `Rule`: Represents a grammar production with a left non-terminal and a list of right-hand symbols.
  - `Tree`: Represents parse trees, with methods to output the terminal sequence and to render the tree in bracketed notation.
  - `join(tokens)`: Utility function to format a list of tokens into a readable string.

- `source/generate.py`: Functions that generate examples of deontic logic expressions and CFG rules with diverse lexical entries.

- `source/generate_utils.py`: Provides helper functions to generate CFG rules using a masked LLM. Currently using `FloBERT`. The rules generation must be greatly improved.

- `cli.py`: main file that runs the above functions through intuitive CLI commands.

## Deontic logic expressions

- `resources/operators.py`: Defines a list of `Rule` instances and generates the basic set of deontic logic formulas with the following operators: $OB$, $PE$, $FO$, $OP$, $OM$, $NO$. Also includes negation, conjunction and disjunction, as to generate semantically equivalent expressions between operators.

- `resources/free_choice.py`: Defines a list of `Rule` instances and generates the basic free-choice disjunction $PE \; (p \lor q) \to PE \; p \land PE \; q$.

- `resources/axiom_obrm.py`: Defines a list of `Rule` instances and generates the OB-RM axiom: $p \to q \Rightarrow OB \; p \to OB \; q$.

## Usage

TODO
