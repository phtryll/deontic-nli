labels_ollama = {
    "NP": ["NP"],
    "VP": ["V_INF", "V_3SG"],
    "ANTONYMS": ["Verb", "Antonym"],
    "ACTIONS": ["VERB"],
    "COMPLEMENTS": [
        "COMP_EAT", "COMP_DRINK", "THINK",
        "COMP_TRAVEL", "COMP_WORK", "COMP_GO",
        "COMP_TALK", "COMP_ENJOY", "COMP_PLAY"
    ],
    "Adjectives": ["NOUN", "ADJ"]
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

    "ANTONYMS": """

        Generate exactly {k} unique, common verbs in the infinitive form.
        For each verb, provide a semantically opposite verb in the infinitive form.
        Do not use negation with 'not' (e.g., avoid 'not sleep').
        Each verb must be intransitive and form a complete action with a subject alone.

        Output two lists.

        Rules:
        1.	Write exactly {k} items for each VERBS/ANTONYMS, no more, no less.
        2.	No summarizing, no ellipses (…), no grouping.
        3.	Output the full list.

    """,

    "COMPLEMENTS": """

        Here is a list of verbs: eat, drink, think, travel, work, go, talk, enjoy, play.
        For each of these verbs, generate exactly {k} unique complements in the form [determiner] [noun], that can be used as complements to those verbs, e.g. “a sandwich”, “the city”.

        Rules:
        1.	Write exactly {k} items for each verb, no more, no less.
        2.	No summarizing, no ellipses (…), no grouping.
        3.	Output the full list.

    """,

    "Adjectives": """

    Here is the subject: humans - ages, genders, roles, or professions.
    Generate exactly {k} unique English nouns that name a person or type of person, e.g. “boy”, “girl”, “man”, “firefighter”, “lawyer”.
    Generate exactly {k} unique descriptive adjectives that can be applied to humans. Include a mix of traits (e.g., curious), physical qualities (e.g., blond), ages (e.g., young), nationalities (e.g., french), and similar attributes.
    
    Rules
        1.	Write exactly {k} adjectives, no more, no less.
        2.	Each adjective must be a single English word, in lowercase.
        3.	No duplicates.
        4.	No summarizing, no ellipses (…), no grouping.
        5.	Output the full list, one adjective per line.

    """,
}


