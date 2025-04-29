decompose_prompt = '''
{instructions}

Here are some examples:
{examples}

Question: {question}
{Thoughts_and_answers}
'''.strip()


decompose_instructions = '''
Please answer the question step by step by interleaving Thought and Answer.
- Thought: reason about the current situation and formulate a sub-question. Your Thought process should aim to formulate as simple and specific a question as possible, which should include a clear description of the key entities’ features.
- Answer:  answer the sub-question proposed in the Thought step.

Starting below, you must follow the following format:
Question: a complex question
Thought 1: The first sub-question
Answer 1: answer the first sub-question
... (the Thought and Answer steps can repeat N times)
Thought n: the final thought
Answer n: FINISH[your final answer]

Note:
1. It is better NOT TO use pronouns in Answer and Thought step, but to use the corresponding results obtained previously. For example, instead of “What is the most popular movie directed by this person”, you should output “Get the most popular movie directed by Martin Scorsese”.
2. Your final answer should be an entity, e.g., a date, place name, and person name. You should always bold the key information with **.
3. You should always give the answer your trust most despite not knowing it exactly. Try to avoid giving "I do not know'.
'''.strip()