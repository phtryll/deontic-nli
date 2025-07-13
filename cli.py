import sys
import json
import logging
import argparse
from argparse import RawTextHelpFormatter
from functools import partial
from pathlib import Path

# Import CFG and generation source code
from source.cfg import CFG
from source.generate import generate_examples, generate_with_ollama, format_rules, format_examples
from resources.prompts import prompts_ollama, labels_ollama

# Grammars
from resources.axiom_obrm import obrm
from resources.axiom_obexh import exh
from resources.free_choice import fcp
from resources.operators import operators

# Suppress useless transformers messages
logging.getLogger("transformers.modeling_utils").setLevel(logging.ERROR)

# Cleaner --help display
MyFormatter = partial(RawTextHelpFormatter, max_help_position=70, width=100)

# Current grammars to generate examples with
GRAMMARS = {
    "obrm": obrm,
    "obexh": exh,
    "fcp": fcp,
    "operators": operators
}

# Current models to generate text
MODELS = ["mistral", "deepseek-r1", "llama-3.1"]

def main():
    
    parser = argparse.ArgumentParser(
        prog="cli.py",
        formatter_class=MyFormatter,
        description="Deontic NLI - CLI utility"
    )

    # Select one or more grammars
    parser.add_argument(
        "-g", "--grammar",
        choices=GRAMMARS,
        nargs="+",
        metavar=("GRAMMAR1", "GRAMMAR2"),
        help=(
            f"select grammar(s) to generate examples: "
            f"{', '.join(GRAMMARS.keys())}"
        )
    )

    # Select one or more grammars
    parser.add_argument(
        "-m", "--model",
        choices=MODELS,
        metavar="MODEL",
        default=MODELS[0],
        help=(
            f"select model for text generation: "
            f"{', '.join(MODELS)} (default: {MODELS[0]})"
        )
    )

    # Option to print the selected CFG(s)
    parser.add_argument("--show-grammar", action="store_true", help="print the CFG grammar(s)")

    # Option to generate N examples from the grammar. Mode can be 'cfg' for uniform or 'pcfg' for probabilistic generation.
    parser.add_argument(
        "--generate-examples",
        nargs='?',
        const=100,
        type=int,
        default=None,
        metavar="N",
        help="generate N examples (default: 100)"
    )

    # Option to generate N lexical rules using the masked language model and RoBERTa
    parser.add_argument(
        "--generate-rules",
        nargs='?',
        const=100,
        type=int,
        default=None,
        metavar="N",
        help="generate N lexical rules from previously generated lexical pool (default: 100)"
    )

    parser.add_argument(
        "-s", "--save",
        metavar="FILE",
        help="save generated rules under data/<FILE>"
    )

    # Store arguments
    args = parser.parse_args()

    # Always initialize an empty grammar dict
    grammars = {}
    
    # Check if grammar has been defined
    if (args.generate_examples or args.show_grammar) and not args.grammar:
        parser.error("argument -g/--grammar is required for generating examples or showing grammar.")
    
    # Ensure that when generating and saving, a filename is provided
    if (args.generate_rules is not None or args.generate_examples is not None) and args.save is None:
        parser.error("you must specify a filename with -s/--save, e.g.: foobar.json")

    # Create a dictionary with all the specified grammars
    if args.grammar:
        grammars = {
            name: CFG(rules=GRAMMARS[name], axiom="S")
            for name in args.grammar
        }

    # Display the CFG(s) to the user
    if args.show_grammar:
        for name, grammar in grammars.items():
            print(f"\n----Context-free grammar for {name}----\n")
            print(grammar)

    # Generate examples
    if args.generate_examples:
        examples_dict = {}
        for name, grammar in grammars.items():
            examples = generate_examples(grammar, args.generate_examples, print_tree=False)
            examples_dict[name] = examples
        
        # Format examples as tuples of premise/hypothesis
        formatted_examples = format_examples(examples_dict)

        for name, examples_list in examples_dict.items():
            print(f"\n----Generated examples for {name}----\n")
            for example in examples_list:
                print(example)
        
        if args.save:
            save_path = Path(__file__).parent / "data" / args.save
            
            with open(save_path, "w", encoding="utf-8") as f:
                json.dump(formatted_examples, f, ensure_ascii=False, indent=4)
            
            print(f"\nSaved generated examples to {save_path}")

    # Generate lexical rules
    if args.generate_rules:
        output_dict = {}
        for label, prompt in prompts_ollama.items():
            prompt = prompt.format(k=args.generate_rules)
            output = generate_with_ollama(prompt, args.model)
            output_dict[label] = output
        
        # Format to CFG rules
        new_rules = format_rules(output_dict)

        for label, output in new_rules.items():
            print(f"\n--- {label} ---\n")
            for item in output:
                print(item)

        if args.save:
            save_path = Path(__file__).parent / "data" / args.save
            
            with open(save_path, "w", encoding="utf-8") as f:
                json.dump(new_rules, f, ensure_ascii=False, indent=4)
            
            print(f"\nSaved generated rules to {save_path}")

# Run CLI
if __name__ == "__main__":
    main()
