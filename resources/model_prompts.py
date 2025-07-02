# Dict[PROMPT_LABEL: List[MASK_LABELS]]
labels = {
    "LOCATIONS": ["CITY", "COUNTRY"]
}

# Dict[PROMPT_LABEL: List[Prompts with 1 or more masks]]
prompts = {
    "LOCATIONS": [
        "The city of <mask> is in the country of <mask>.",
        "We went to <mask>, and visited the little town of <mask>. It was beautiful!"
    ]
}