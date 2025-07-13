import json
import logging
import argparse
from pathlib import Path
from functools import partial
from argparse import RawTextHelpFormatter

# Import CFG and generation source code
from source.cfg import CFG
from source.generate import generate_examples, generate_items, format_rules, format_examples
from resources.prompts import prompts_ollama

# Grammars
from resources.axiom_obrm import obrm, obrm_base
from resources.axiom_obexh import exh, exh_base
from resources.free_choice import fcp, fcp_base
from resources.operators import operators, operators_base

# Suppress useless transformers messages
logging.getLogger("transformers.modeling_utils").setLevel(logging.ERROR)

# Cleaner --help display
MyFormatter = partial(RawTextHelpFormatter, max_help_position=70, width=100)

# Current grammars to generate examples with
GRAMMARS = {
    "obrm": (obrm, obrm_base),
    "obexh": (exh, exh_base),
    "fcp": (fcp, fcp_base),
    "operators": (operators, operators_base)
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
    parser.add_argument(
        "--show-grammar",
        choices=["base", "full"],
        metavar="GRAMMAR",
        help="print the CFG grammar(s): base, full"
    )

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

    # Option to generate N lexical rules using ollama for text generation
    parser.add_argument(
        "--generate-rules",
        nargs='?',
        const=100,
        type=int,
        default=None,
        metavar="N",
        help="generate N lexical rules from previously generated lexical pool (default: 100)"
    )

    # Specify what prompt(s) we want to use
    parser.add_argument(
        "-l", "--labels",
        nargs="+",
        choices=list(prompts_ollama.keys()),
        metavar="LABEL",
        help="select which prompt labels to generate rules for (default: all)"
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

    # Create a dictionary with all the specified grammars
    if args.grammar:
        grammars = {
            name: CFG(rules=GRAMMARS[name][0], axiom="S")
            for name in args.grammar
        }

    # Display the CFG(s) to the user
    if args.show_grammar:
        if args.show_grammar == "full":
            for name, grammar in grammars.items():
                print(f"\n----Context-free grammar for {name}----\n")
                print(grammar)

        if args.show_grammar == "base":
            base_grammars = {
                name: CFG(rules=GRAMMARS[name][1], axiom="S")
                for name in args.grammar
            }
            
            for name, grammar in base_grammars.items():
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
        selected_labels = args.labels if args.labels else prompts_ollama.keys()
        
        for label in selected_labels:
            prompt = prompts_ollama[label]
            prompt = prompt.format(k=args.generate_rules)
            output = generate_items(prompt, args.model)
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
