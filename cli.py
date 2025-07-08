import os
import sys
import json
import argparse
import logging
from pathlib import Path
from transformers import AutoTokenizer, AutoModelForMaskedLM
from source.generate import generate_examples, generate_rules
from source.generate_utils import generate_lexical_pool, save_rules_json, save_lexical_pool_json
from source.cfg import CFG
from source.cfg_utils import Rule
from resources.axiom_obrm import my_rules
from resources.model_prompts import prompts, labels


# Suppress useless transformers messages
logging.getLogger("transformers.modeling_utils").setLevel(logging.ERROR)

# CLI tool for generating deontic logic examples and lexical resources
def main():
    parser = argparse.ArgumentParser(description="Deontic NLI CLI utility")

    # Option to print the underlying CFG grammar rules
    parser.add_argument("--show-grammar", action="store_true", help="Print the CFG grammar")

    # Option to generate N examples from the grammar. Mode can be 'cfg' for uniform or 'pcfg' for probabilistic generation.
    parser.add_argument(
        "--generate-examples",
        nargs=2,
        metavar=("N", "MODE"),
        help="Generate N examples; MODE should be 'cfg' or 'pcfg'",
        default=None,
    )

    # Option to generate a pool of lexical items for each category using the masked language model
    parser.add_argument(
        "--generate-lexical-pool",
        nargs='?',
        const=20,
        type=int,
        default=None,
        metavar="N",
        help="Generate N lexical items for specific categories"
    )
    
    # Option to generate N lexical rules using the masked language model and RoBERTa
    parser.add_argument(
        "--generate-rules",
        nargs='?',
        const=20,
        type=int,
        default=None,
        metavar="N",
        help="Generate N lexical rules using RoBERTa"
    )

    # Option to save output to JSON files under data/
    parser.add_argument(
        "--save",
        action="store_true",
        help="Save output to JSON files under data/"
    )

    # Option to reset a data file under data/
    parser.add_argument(
        "--reset",
        choices=["lexical_items", "lexical_rules"],
        metavar="TARGET",
        help="Reset the specified data file (lexical_items or lexical_rules)"
    )

    args = parser.parse_args()

    # Handle reset of data files: clear contents without deleting the file
    if args.reset:
        file_map = {
            "lexical_items": "lexical_items_pool.json",
            "lexical_rules": "lexical_rules_pool.json"
        }
        
        target = args.reset
        data_dir = Path.cwd() / "data"
        file_path = data_dir / file_map[target]
        
        # Ensure data directory exists
        data_dir.mkdir(parents=True, exist_ok=True)
        
        # empty_content = 

        # Write empty JSON content (truncate or create file)
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump({}, f, ensure_ascii=False, indent=2)
        print(f"Cleared contents of {target} file at {file_path}")
        sys.exit(0)

    # Initialize tokenizer and model
    tokenizer = AutoTokenizer.from_pretrained("FacebookAI/xlm-roberta-large")
    model = AutoModelForMaskedLM.from_pretrained("FacebookAI/xlm-roberta-large")
    
    # Initialize grammar
    grammar = CFG(rules=my_rules, axiom="S")

    if args.show_grammar:
        
        # Display the CFG grammar to the user
        print("\n----Context-free grammar----\n")
        print(grammar)

    if args.generate_examples:
        
        # Parse and validate generate-examples arguments
        count_str, mode = args.generate_examples
        
        try:
            count = int(count_str)
        except ValueError:
            parser.error("generate-examples requires an integer count and mode 'cfg' or 'pcfg'")
        
        mode_lower = mode.lower()
        
        if mode_lower not in ("cfg", "pcfg"):
            parser.error("generate-examples mode must be 'cfg' or 'pcfg'")
        
        use_probabilistic = (mode_lower == "pcfg")
        
        # Create a CFG instance with probabilistic mode if requested
        grammar_to_use = CFG(rules=my_rules, axiom="S", probabilistic=use_probabilistic)
        
        print(f"----Generated examples ({mode_lower.upper()})----\n")
        generate_examples(grammar_to_use, count, print_tree=False)

    if args.generate_rules:
        # Generate lexical inference rules using the language model
        rules = generate_rules(prompts, tokenizer, model, top_k=args.generate_rules, labels=labels)
        if args.save:
            save_rules_json(rules)
        else:
            for rule in rules:
                print(rule)
    
    if args.generate_lexical_pool:
        # Generate lexical category pools using the masked language model
        pool = generate_lexical_pool(prompts, tokenizer, model, top_k=args.generate_lexical_pool)
        if args.save:
            save_lexical_pool_json(pool)
        else:
            for category, items in pool.items():
                for item in items:
                    print(f"{category}: {item}")

if __name__ == "__main__":
    main()
