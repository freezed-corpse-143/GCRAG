ground_prompt = '''
{instructions}

Here are some examples:
{examples}

Input:
Question: {question}
{retrieved_documents}
Thought: {thought}
Old answer: {answer}
New answer and supporting fact ids:
'''.strip()

ground_instructions = '''
You will be provided with documents (labeled Document 1, Document 2, etc.), a question, and an old answer. Your task is to:
1. Verify and edit the old answer using only information from the provided documents.
2. If no document can confirm/contradict/improve the old answer, output it as the new answer and nothing after "Supporting fact ids".
3. If you edit the old answer, please attach the reason why you edit to tail of new answer without newline/line break.
4. Please cite the document(s) used to verify/edit the answer. If "Document <id>: ..." is helpful in editting old answer, please add "<id>" in output supporting fact ids.
5. If you cite multiple ids, separate them with commas. For example, generate "Supporting fact ids: 2,4" if you cite "Document 2: ..." and "Document 4: ...".


Example format:
Input:
Question: What is topic A about?
Document 1: "Text about topic A is about music"
Document 2: "Text about topic B..."
Document 3: "Text about topic C..."
...
Old Answer: Topic A is about computer.
New answer and supporting fact ids:
New answer: Topic A is about music, according to "Document 1".
Supporting fact ids: 1
'''.strip()
