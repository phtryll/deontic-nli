labels_ollama = {
    "NP": ["NP"],
    "VP": ["V_INF", "V_3SG"]
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

    """

}
