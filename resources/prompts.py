labels_ollama = {
    "NP": ["NP"],
    "VP": ["V_INF", "V_3SG"],
    "VP_INF_NEG": ["V_INF_neg", "V_INF_ant"],
}

prompts_ollama = {

    "NP": """
    
    Generate exactly {k} unique and simple noun phrases.
    They should consist of a determiner and a noun representing a person (e.g., 'the boy', 'the man', 'the teacher', 'my friend').
    
    """,
    
    "VP": """
    
    Generate exactly {k} unique verbs.
    For each verb, provide its infinitive form (e.g., 'sleep') and its third person singular form (e.g., 'sleeps').
    They should combine with a subject to form a complete action without requiring an object or complement.
    For example, 'sleeps', 'runs'; avoid 'advocates', which typically needs a complement.

    """,

    "VP_INF_NEG": """

    Generate exactly {k} unique, common verbs in the infinitive form.
    For each verb, provide a semantically opposite verb in the infinitive form.
    Do not use negation with 'not' (e.g., avoid 'not sleep').
    Each verb must be intransitive and form a complete action with a subject alone.

    # Output two lists with these exact headings:

    # V_INF_neg:
    # - verb1
    # - verb2
    # ...

    # V_INF_ant:
    # - antonym1
    # - antonym2
    # ...


    """,
}


