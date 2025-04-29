revise_prompt = '''
{instructions}

{retrieval_documents}

Question: {question}
{Thoughts_and_answers}
'''.strip()

revise_instrcutions = '''
You will be provided with {n} documents delimited by triple quotes and a question.
Your task is to answer the question using only the provided document and to cite the passage(s) of the document used to answer the question.
Please be careful:
1. If the document does not contain the information needed to answer this question then simply write `Insufficient information`.
2. If an answer to the question is provided, it must be annotated with a citation. Use the following format to cite relevant passages ({{"citation": …}}).
'''.strip()

