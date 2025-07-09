import sys
import json
import logging
import argparse
from argparse import RawTextHelpFormatter
from functools import partial
from pathlib import Path
from transformers import AutoTokenizer, AutoModelForMaskedLM


# Import CFG and generation source code
from source.cfg import CFG
from source.generate import generate_examples, generate_rules
from source.generate_utils import generate_lexical_pool, save_rules, save_lexical_pool
from resources.model_prompts import prompts, labels


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
    "OB_RM": obrm,
    "OB_EXH": exh,
    "FCP": fcp,
    "Deontic_Operators": operators
}

# Current models to generate lexical items with
MODELS = {
    "RoBERTa": "FacebookAI/xlm-roberta-large"
}

# Files to store lexical items, rules and examples
FILE_MAP = {
            "examples": "examples.json",
            "lexical_items": "lexical_items_pool.json",
            "lexical_rules": "lexical_rules_pool.json"
        }


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
        default=list(MODELS.keys())[0],
        help=(
            f"select model for masked LM: "
            f"{', '.join(MODELS.keys())} (default: {list(MODELS.keys())[0]})"
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

    # Option to generate a pool of lexical items for each category using the masked language model
    parser.add_argument(
        "--generate-lexical-pool",
        nargs='?',
        const=100,
        type=int,
        default=None,
        metavar="N",
        help="generate N lexical items for specific categories using masked LM (default: 100)"
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

    # Option to save output to JSON files under data/
    parser.add_argument(
        "-s", "--save",
        action="store_true",
        help="save output in JSON format in the 'data' directory"
    )

    # Option to reset a data file under data/
    parser.add_argument(
        "--reset",
        choices=FILE_MAP,
        nargs="+",
        metavar=("FILE1", "FILE2"),
        help=(
            f"reset the specified data file(s): "
            f"{', '.join(FILE_MAP.values())}"
        )
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
            name: CFG(rules=GRAMMARS[name], axiom="S")
            for name in args.grammar
        }

    # Display the CFG(s) to the user
    if args.show_grammar:
        for name, grammar in grammars.items():
            print(f"\n----Context-free grammar for {name}----\n")
            print(grammar)


    # Reset data files: clean the file contents without erasing the files
    if args.reset:
        targets = args.reset
        data_dir = Path.cwd() / "data"
        data_dir.mkdir(parents=True, exist_ok=True)

        for target in targets:
            file_path = data_dir / FILE_MAP[target]
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump({}, f, ensure_ascii=False, indent=2)
            print(f"Cleared contents of {target} file at {file_path}")
        
        sys.exit(0)


    # Initialize tokenizer and model
    tokenizer = AutoTokenizer.from_pretrained(MODELS[args.model])
    model = AutoModelForMaskedLM.from_pretrained(MODELS[args.model])

    if args.generate_examples:
        
        # Parse and validate generate-examples arguments
        count_str, mode = args.generate_examples
        
        try:
            count = int(count_str)
        except ValueError:
            parser.error("generate-examples requires an integer count and mode 'cfg' or 'pcfg'")
        
        mode_lower = mode.lower()
        
        # Create a CFG instance with probabilistic mode if requested
        grammar_to_use = CFG(rules=args.grammar, axiom="S")
        
        print(f"----Generated examples ({mode_lower.upper()})----\n")
        generate_examples(grammar_to_use, count, print_tree=False)

    if args.generate_rules:
        # Generate lexical inference rules using the language model
        rules = generate_rules(prompts, tokenizer, model, top_k=args.generate_rules, labels=labels)
        if args.save:
            save_rules(rules)
        else:
            for rule in rules:
                print(rule)
    
    if args.generate_lexical_pool:
        # Generate lexical category pools using the masked language model
        pool = generate_lexical_pool(prompts, tokenizer, model, top_k=args.generate_lexical_pool)
        if args.save:
            save_lexical_pool(pool)
        else:
            for category, items in pool.items():
                for item in items:
                    print(f"{category}: {item}")


# Run CLI
if __name__ == "__main__":
    main()
