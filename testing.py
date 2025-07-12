from pydantic import BaseModel
from ollama import chat

class Test(BaseModel):
  examples: list[str]

prompt = """

Generate 100 examples with lexical diversity that respect the following surface structure:
'If <name> <verb> <city>, then <name> <verb> <country>'.
The name and the verb should be the same within each example.

"""

response = chat(
    messages=[
        {
        'role': 'user',
        'content': prompt
        }
    ],
    model='mistral',
    format=Test.model_json_schema(),
)

content = response.message.content
if content is None: raise ValueError("No content in model response")

country = Test.model_validate_json(content)
for example in country.examples:
   print(example)


# def generate_fcp_tuples(num_samples=None):
#     """
#     Generate free-choice permission examples as (premise, hypothesis) tuples.
#     """
#     raw_examples = grammar.generate("S", num_samples)
#     tuples = []
#     for ex in raw_examples:
#         if "[H]" in ex:
#             prem, hyp = ex.split("[H]", 1)
#             prem = prem.strip()
#             hyp = "[H]" + hyp.strip()
#             tuples.append((prem, hyp))
#     return tuples