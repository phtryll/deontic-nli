import time
from ollama import chat
from typing import List
from pydantic import BaseModel, ConfigDict, conlist

from source.cfg import CFG
from source.cfg_utils import join


def build_relation_schema(field_names: List[str], k: int):
    n = len(field_names)
    class LexicalRelationSchema(BaseModel):
        model_config = ConfigDict(extra="forbid")

        items: conlist( # type: ignore
            conlist(str, min_length=n, max_length=n),
            min_length=k,
            max_length=k
        )

    return LexicalRelationSchema


def generate_lexical_items(prompt: str, field_names: List[str], k: int, model: str):
    Schema = build_relation_schema(field_names, k)
    json_schema = Schema.model_json_schema()
    json_schema["additionalProperties"] = False

    system_prompt = (
        "You are a JSON generator. "
        "You must output only valid JSON that conforms exactly to the provided schema. "
        f"Generate exactly {k} rows. "
        "Each row must be a joint lexical choice aligned with the fields."
    )

    system_msg = {"role": "system", "content": system_prompt}
    user_msg = {
        "role": "user",
        "content": (
            f"Fields: {field_names}\n"
            f"{prompt}"
        ),
    }

    start = time.time()

    response = chat(
        messages=[system_msg, user_msg],
        model=model,
        format=json_schema,
        stream=False,
    )

    content = response["message"]["content"]
    instance = Schema.model_validate_json(content)

    elapsed = time.time() - start
    print(f"Generation took {elapsed:.2f}s")

    return {"fields": field_names, "items": instance.items}


def generate_examples(grammar: CFG, num_examples: int = 20, print_tree: bool = False) -> List[str]:
    examples: List[str] = []

    for _ in range(num_examples):
        tree = grammar.generate(False)
        tokens = tree.output()
        
        if print_tree:
            print("sampled tree:", tree)
            print("yield:", tokens)
        
        example = join(tokens)
        examples.append(example)

    return examples
