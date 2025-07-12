# Dict[PROMPT_LABEL: List[str: MASK_LABELS]]
labels_masked = {
    "VERBS": ["VERB"],
    "NAMES": ["NAME"],
    "AGENTS": ["AGENT"],
    "ADJECTIVES": ["ADJ"],
    "LOCATIONS": ["CITY", "COUNTRY"]
}

# Dict[PROMPT_LABEL: List[str: prompts with 1 or more masks]]
prompts_masked = {
    "VERBS": [
        "The man loves to <mask>.",
        "The woman loves to <mask>.",
        "The man <mask> in the park.",
        "The woman <mask> in the park.",
        "That person <mask> to help his friends."
    ],
    "NAMES": [
        "My best friend is <mask>.",
        "My father is called <mask>.",
        "My wife's name is <mask>, a lovely name.",
    ],
    "AGENTS": [
        "The <mask> fixed the car.",
        "The <mask> taught the class.",
        "An experienced <mask> solved the problem.",
        "The <mask> arrived at the site early.",
        "Every <mask> must renew their license annually."
    ],
    "ADJECTIVES": [
        "She has <mask> hair.",
        "He lives in a <mask> house.",
        "They adopted a <mask> puppy.",
        "The <mask> car sped by.",
        "The painting has <mask> colors."
    ],
    "LOCATIONS": [
        "The city of <mask> in <mask> is known for its beautiful architecture.",
        "During my trip, I visited <mask>, a city in <mask>.",
        "The historic city <mask> is located in <mask>.",
        "I explored <mask> in <mask> and enjoyed the local culture.",
        "The famous festival in <mask> draws tourists to <mask>."
    ]
}