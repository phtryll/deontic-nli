labels_ollama = {
    "VP_b": ["V_INF", "V_3SG"]
}

prompts_ollama = {
    "NP": "Generate exactly {k} unique simple noun phrases consisting of a determiner and a nou that is an agent, for example: 'the boy', 'the man', 'the teacher', 'my friend'.",
    "VP_a": "Generate exactly {k} unique simple verbs in the third person present tense, for example: 'sleeps', 'thinks'. Avoid verbs that require an object like 'goes', 'sees' or 'maintains'.",
    "VP_b": "Generate exactly {k} unique verbs, for each verb give its infinitive from (ex: 'sleep') and its 3rd person singular form (ex: 'sleeps')."
}