# Deontic NLI

This project explores how NLI systems understand deontic (normative) language.

We first translate deontic logic formulas into natural language, and then feed them into an NLI system for evaluation under the classic "entailment", "contradiction", "neutral" classification task.

## Table of Contents

- [Deontic NLI](#deontic-nli)
  - [Table of Contents](#table-of-contents)
  - [Installation \& Running](#installation--running)
  - [CLI Usage](#cli-usage)
    - [Arguments](#arguments)
    - [Examples](#examples)

## Installation & Running

To get started with this repository, clone it and navigate into the directory:

```bash
git clone <repo-url>
cd deontic-nli
```

It is recommended to create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

You can run the CLI tool with:

```bash
python cli.py
```

Use the help flag to see available options:

```bash
python cli.py --help
```

## CLI Usage

This project provides a command-line utility (`cli.py`) for generating and evaluating grammars.

### Arguments

Below is a description of each argument available in the CLI tool:

- **`-g, --grammar`**: Select a grammar group to work with. Valid keys are `obrm`, `obexh`, `fcp`, `operators`.

- **`--show`**: Show the selected CFG. You can choose between `base` (without lexical rules) or `full` (with lexical rules).

- **`-m, --model`**: Select a model for lexical item generation. Defaults to `mistral`. Available options are `mistral`, `deepseek-r1`, and `llama3.1`.

- **`--generate-examples [N]`**: Generate N examples from the selected grammar. Defaults to 100 if no value is provided.

- **`--generate-rules [N]`**: Generate N lexical items and format them into CFG rules. Defaults to 100 if no value is provided.

- **`--labels`**: Choose which prompt labels to use for lexical items generation. If none are specified, all labels are used by default.

- **`-s, --save FILENAME`**: Save generated data to a file under the `data/` directory with the given filename.

- **`-e, --evaluate FILENAME`**: Evaluate a JSON file of examples with the model. Provide the path to the JSON file.

| Argument                   | Description                                         | Default     | Options                              |
|----------------------------|-----------------------------------------------------|-------------|--------------------------------------|
| `-g, --grammar`            | Select a grammar group                              | None        | `obrm`, `obexh`, `fcp`, `operators`  |
| `--show`                   | Show the selected CFG                               | None        | `base`, `full`                       |
| `-m, --model`              | Choose the generation model                         | `mistral`   | `mistral`, `deepseek-r1`, `llama3.1` |
| `--generate-examples [N]`  | Generate N examples                                 | `100`       | Any integer                          |
| `--generate-rules    [N]`  | Generate N lexical items and CFG rules              | `100`       | Any integer                          |
| `--labels`                 | Specify which prompt labels to use                  | All         | Space-separated list                 |
| `-s, --save FILENAME`      | Save generated data                                 | None        | Filename                             |
| `-e, --evaluate FILENAME`  | Evaluate a JSON file of examples with the model     | None        | Path to JSON file                    |

### Examples

- Generate 50 examples using the `fcp` grammar group:
  
```bash
  python cli.py -g fcp --generate-examples 50
```

- Show the basic CFG rules for the `fcp` grammar group:

```bash
python cli.py -g fcp --show base
```

- Generate 20 lexical item rules with for each of two labels and save to a file:

```bash
python cli.py --generate-rules 20 --labels NP VP -s rules_NP_VP.json
```

- Evaluate a JSON file of examples:

```bash
python cli.py -e data/examples.json
```
