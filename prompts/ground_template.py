ground_prompt = '''
{instructions}

Here are some examples:
{examples}

{retrieved_documents}
Question: {question}
Candidate Answer: {answer}
'''.strip()

ground_instrcutions = '''
You will be provided with {n} documents delimited by triple quotes and a question.
Your task is to edit the candidate answer using only the provided document and to cite the passage(s) of used to edit the candidate answer.
Your answers need to be precise (less than 20 words). Do not introduce information that is not relevant to the question.
Please be careful:
1. If there is no document can contain the information need to edit the answer, your output should be {{"answer": "<candidate answer>", "citation": [] }}.
2. If an answer to the question is provided, it must be annotated with a citation. Use the following format to cite relevant documents ({{"citation": […]}}).
3. Your output should be JSON format: {{"answer": "<the edited answer>","citation":["<cite the document index used to edit the candidate answer>", …]}}.
'''.strip()

