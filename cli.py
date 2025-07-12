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
from source.generate_utils import generate_lexical_pool, save_rules, save_lexical_pool, save_examples
from resources.prompts_masked import prompts_masked, labels_masked

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

# Current models to generate lexical items with MLM
MODELS_MLM = {
    "roberta": "FacebookAI/xlm-roberta-large",
    "bert": "google-bert/bert-large-uncased",
    "modernbert": "answerdotai/ModernBERT-large"
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
        choices=MODELS_MLM,
        metavar="MODEL",
        default=list(MODELS_MLM.keys())[0],
        help=(
            f"select model for masked LM: "
            f"{', '.join(MODELS_MLM.keys())} (default: {list(MODELS_MLM.keys())[0]})"
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

    # Testing flag: optional top_k (default 100) + one or more tasks
    parser.add_argument(
        "--testing",
        nargs='*',
        metavar=("TOP_K", "TASK"),
        help="run testing tasks with optional top_k (default: 100) and one or more subcommands (e.g., 100 lexical-pool)"
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
            f"{', '.join(FILE_MAP.keys())}"
        )
    )

    # Store arguments
    args = parser.parse_args()

    # Always initialize an empty grammar dict
    grammars = {}

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

    # Generate examples
    if args.generate_examples:
        examples_dict = {}
        for name, grammar in grammars.items():
            examples = generate_examples(grammar, args.generate_examples, print_tree=False)
            examples_dict[name] = examples
        if args.save:
            save_examples(examples_dict)
        else:
            for name, examples_list in examples_dict.items():
                print(f"\n----Generated examples for {name}----\n")
                for example in examples_list:
                    print(example)

    # Generate lexical rules
    if args.generate_rules:
        tokenizer = AutoTokenizer.from_pretrained(MODELS_MLM[args.model])
        model = AutoModelForMaskedLM.from_pretrained(MODELS_MLM[args.model])
        rules = generate_rules(prompts_masked, tokenizer, model, top_k=args.generate_rules, labels=labels_masked)
        if args.save:
            save_rules(rules)
        else:
            for category, slot_dict in rules.items():
                print(f"\n--- {category} lexical-rules ---\n")
                for slot_label, rule_list in slot_dict.items():
                    for rule in rule_list:
                        print(f"{slot_label}: {rule}")
    
    # Post-parse handling for --testing argument
    if args.testing is not None:
        if len(args.testing) == 0:
            args.testing = ["100", "lexical-pool"]
        elif not args.testing[0].isdigit():
            args.testing = ["100"] + args.testing
        elif len(args.testing) == 1 and args.testing[0].isdigit():
            args.testing = args.testing + ["lexical-pool"]

    # Lexical items generation
    if args.testing:
        top_k = int(args.testing[0])
        tasks = args.testing[1:]

        if "lexical-pool" in tasks:
            tokenizer = AutoTokenizer.from_pretrained(MODELS_MLM[args.model])
            model = AutoModelForMaskedLM.from_pretrained(MODELS_MLM[args.model])
            pool = generate_lexical_pool(prompts_masked, tokenizer, model, top_k=top_k)
            if args.save:
                save_lexical_pool(pool)
            else:
                for category, items in pool.items():
                    print(f"\n--- {category} lexical-pool ---\n")
                    for item in items:
                        print(item)

# Run CLI
if __name__ == "__main__":
    main()
