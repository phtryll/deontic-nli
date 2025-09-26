import json
import logging
import argparse
from pathlib import Path
from functools import partial
from argparse import RawTextHelpFormatter
from source.evaluate import evaluate, model, tokenizer

# Import CFG and generation source code
from source.cfg import CFG
from source.generate import generate_examples, generate_items, format_rules, format_examples
from resources.prompts import prompts_ollama, labels_ollama

# Grammars
from resources.axiom_obrm import obrm, obrm_base
from resources.axiom_obexh import exh, exh_base
from resources.free_choice import fcp, fcp_base
from resources.operators import operators, operators_base

# Suppress useless transformers messages
logging.getLogger("transformers.modeling_utils").setLevel(logging.ERROR)

# Cleaner --help display
MyFormatter = partial(RawTextHelpFormatter, max_help_position=50, width=120)

# ---------
# META-VARS
# ---------

# Current grammars to generate examples with
GRAMMARS = {
    "obrm": (obrm, obrm_base),
    "obexh": (exh, exh_base),
    "fcp": (fcp, fcp_base),
    "operators": (operators, operators_base)
}

# Current models to generate text
MODELS_GEN = ["mistral", "deepseek-r1", "llama3.1"]

# Current models to evaluate text
MODELS_EVAL = []

# ----------------
# PARSER ARGUMENTS
# ----------------

def main():
    
    # Title
    parser = argparse.ArgumentParser(
        prog="cli.py",
        formatter_class=MyFormatter,
        description="Deontic NLI - CLI utility"
    )

    # Select one grammar group
    parser.add_argument(
        "-g", "--grammar",
        metavar="GRAMMAR",
        help=(
            f"select a grammar group by key; "
            f"valid keys: {', '.join(GRAMMARS.keys())}"
        )
    )

    # Option to view the selected CFG from the grammar group
    parser.add_argument(
        "--show",
        choices=["base", "full"],
        metavar="TYPE",
        help="view the selected CFG, either with lexical rules (TYPE: full) or without (TYPE: base)"
    )

    # Select a generation models (default choice: 'mistral')
    parser.add_argument(
        "-m", "--model",
        choices=MODELS_GEN,
        metavar="MODEL",
        default=MODELS_GEN[0],
        help=(
            f"select a model for lexical item(s) generation: "
            f"{', '.join(MODELS_GEN)} (default: {MODELS_GEN[0]})"
        )
    )

    # Option to generate N examples from the grammar
    parser.add_argument(
        "--generate-examples",
        nargs='?',
        const=100,
        type=int,
        default=None,
        metavar="N",
        help="generate N examples from the selected grammar (default: 100)"
    )

    # Option to generate N lexical rules using ollama for text generation
    parser.add_argument(
        "--generate-grammars",
        nargs='?',
        const=100,
        type=int,
        default=None,
        metavar="N",
        help="generate N lexical items and format them into CFG rules using an LLM (default: 100)"
    )

    # Specify what prompt(s) we want to use
    parser.add_argument(
        "--labels",
        nargs="+",
        choices=list(prompts_ollama.keys()),
        metavar="LABEL",
        help="select which prompt labels to generate lexical items for (default: all)"
    )

    # Save generated rules/examples toggle
    parser.add_argument(
        "-s", "--save",
        metavar="FILENAME",
        help="save generated rules/examples under data/<FILENAME>"
    )

    # Evaluate NLI on a JSON file of pairs
    parser.add_argument(
        "-e", "--evaluate",
        metavar="FILENAME",
        type=Path,
        help="evaluate a JSON file with examples"
    )

    args = parser.parse_args()

# ----------
# EVALUATION
# ----------

    if args.evaluate:
        # Verify output directory exists
        results_dir = Path(__file__).parent / "results"
        results_dir.mkdir(exist_ok=True)

        # Load examples
        with open(args.evaluate, "r", encoding="utf-8") as f:
            examples = json.load(f)
        
        # Format examples into List[Tuple] and evaluate
        for key, tuples in examples.items():
            pairs = [tuple(item) for item in tuples]
            evaluate(pairs, model, tokenizer, key_name=key, results_dir=str(results_dir))
        return

# ---------------
# GRAMMAR LOADING
# ---------------

    # Init empty dict
    selected_grammars = {}

    if args.grammar:
        # Check if the input matches available grammar keys
        if args.grammar not in GRAMMARS:
            parser.error(f"Unknown grammar key '{args.grammar}'. Valid keys: {', '.join(GRAMMARS.keys())}")

        # Extract the CFGs within the selected grammar group
        grammars, grammars_base = GRAMMARS[args.grammar]

        # Prompt the user to select a grammar within the group
        if isinstance(grammars, dict):
            available_grammars = list(grammars.keys())

            # Display the available grammars to the user
            print(f"Grammar group '{args.grammar}' has multiple sub-grammars. Available options:")
            for i, name in enumerate(available_grammars, start=1):
                print(f"    {i}. {name}")

            selected_indices = None  # No indices selected until user input is verified
            prompt = "Select grammar number(s) (e.g. 1 or 1,3 or 'all'/'*'): "

            # While loop to verify user input
            while selected_indices is None:
                choice = input(prompt).strip()

                # Continue if empty
                if not choice:
                    print("Invalid entry. Please enter number(s) from the list above.")
                    continue

                # Account for all sub-grammars
                if choice.lower() in {"all", "*"}:
                    selected_indices = list(range(len(available_grammars)))
                    break

                # Split at comma
                tokens = choice.replace(",", " ").split()

                indices = []
                valid = True

                # Go through the input tokens for each
                for token in tokens:
                    # If one of the tokens is not a digit start over
                    if not token.isdigit():
                        valid = False
                        break
                    
                    # If its a digit reindex correctly from 0 and check if valid
                    idx = int(token) - 1
                    if idx < 0 or idx >= len(available_grammars):
                        valid = False
                        break

                    # If all is well, add to the indices
                    indices.append(idx)

                # If break, restart
                if not valid:
                    print("Invalid entry. Please enter number(s) from the list above.")
                    continue

                # Selected indices of the grammars
                selected_indices = sorted(set(indices))

            # Build a dictionary of name: grammar
            for idx in selected_indices:
                selected_key = available_grammars[idx]
                selected_grammar = grammars[selected_key]
                selected_grammars[selected_key] = CFG(rules=selected_grammar, axiom="S")

            # ---------------------
            # VIEW SELECTED GRAMMAR
            # ---------------------

            if args.show:
                if args.show == "full":
                    for name, grammar in selected_grammars.items():
                        print(f"\n----Context-free grammar for {name}----\n")
                        print(grammar)

                if args.show == "base":
                    for name in selected_grammars:
                        base_rules = grammars_base[name]
                        base_grammar = CFG(rules=base_rules, axiom="S")
                        print(f"\n----Context-free grammar for {name}----\n")
                        print(base_grammar)

# -----------------
# GENERATE EXAMPLES
# -----------------

    if args.generate_examples:
        examples_dict = {}
        
        for name, grammar in selected_grammars.items():
            examples = generate_examples(grammar, args.generate_examples, print_tree=False)
            examples_dict[name] = examples
        
        formatted_examples = format_examples(examples_dict)

        for name, examples_list in examples_dict.items():
            print(f"\n----Generated examples for {name}----\n")
            for example in examples_list:
                print(example)
        
        if args.save:
            save_path = Path(__file__).parent / "data" / args.save
            
            # Load existing data if the file exists
            if save_path.exists():
                with open(save_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
            else:
                data = {}
            
            # Merge new examples into existing data
            for name, examples_list in formatted_examples.items():
                if name in data and isinstance(data[name], list):
                    data[name].extend(examples_list)
                else:
                    data[name] = examples_list
            
            # Write merged data back to file
            with open(save_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            print(f"\nSaved generated examples to {save_path}")

# --------------
# GENERATE RULES
# --------------

    # Generate lexical grammars
    if args.generate_grammars:
        output_dict = {}
        selected_labels = args.labels if args.labels else prompts_ollama.keys()
        
        for label in selected_labels:
            prompt = prompts_ollama[label]
            field_names = labels_ollama[label]
            prompt = prompt.format(k=args.generate_grammars)
            
            result = generate_items(prompt, args.generate_grammars, field_names, args.model)
            output_dict.update(result)
        
        new_grammars = format_rules(output_dict)

        for label, output in new_grammars.items():
            print(f"\n--- {label} ---\n")
            
            for item in output:
                print(item)

        if args.save:
            save_path = Path(__file__).parent / "data" / args.save
            
            with open(save_path, "w", encoding="utf-8") as f:
                json.dump(new_grammars, f, ensure_ascii=False, indent=4)
            
            print(f"\nSaved generated grammars to {save_path}")

# Run CLI
if __name__ == "__main__":
    main()
