decompose_instructions = '''
Please answer the question by following these steps:
1. Break down the main question into smaller, specific sub-questions
2. For each sub-question:
   - First provide a "Thought:" that clearly states what you're investigating
   - Then provide an "Answer:" with factual information and key details in bold
3. Continue until you can conclusively answer the original question
4. When you can conclusively answer the original question, end with "Answer: FINISH[final answer]"

Rules to follow:
- **Be specific** in Thoughts: Clearly name entities and what you're checking
- **Bold key facts** in Answers: Highlight the most important information
- **No pronouns**: Always use proper names instead of "he/she/they"
- **Be decisive**: Provide the best answer you can even if uncertain
- **One step at a time**: Generate only one new thought/answer pair
- **Be diverse**: For each sub-question, generate multiple semantically equivalent but formally distinct questions without newline as the thought.

Example Format:
Question: [original question]
Thought 1: [first sub-question]
Answer 1: [answer with **key facts**]
Thought 2: [next sub-question]
Answer 2: [answer with **key facts**]
...
Answer: FINISH[final conclusion]
'''.strip()

decompose_prompt = f"{decompose_instructions}" + '''

Here are some examples of how to answer step-by-step:
{examples}

Now answer the following question using the same format:
Input:
Question: {question}
{thoughts_and_answers}
{supporting_facts}
New one thought/answer pair:
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

ground_prompt = f"{ground_instructions}" + '''

Here are some examples:
{examples}

Input:
Question: {question}
{retrieved_documents}
Thought: {thought}
Old answer: {answer}
New answer and supporting fact ids:
'''.strip()

answer_format_instructions = '''
You will be provided with a question and an old answer. Your task is to analyze the old answer and generate a new, concise answer that directly responds to the question. The new answer should:
1. If the question is a yes/no question, answer only "YES" or "NO."
2. If the question requires an entity (e.g., time, person, place), extract the most relevant one as answer without additional explanatory or descriptive information.
2. Be as brief as possible
3. End with "FINISH[answer]" where "answer" is your response

Format your response exactly as shown in the examples.
'''.strip()

answer_format_examples = '''
Question: Nobody Loves You was written by John Lennon and released on what album that was issued by Apple Records, and was written, recorded, and released during his 18 month separation from Yoko Ono?
Old answer: The album issued by Apple Records, and written, recorded, and released during John Lennon's 18 month separation from Yoko Ono is Walls and Bridges. Nobody Loves You was written by John Lennon on Walls and Bridges album. So the answer is: Walls and Bridges.
New answer: FINISH[Walls and Bridges]

Question: What is known as the Kingdom and has National Route 13 stretching towards its border?
Old answer: Cambodia is officially known as the Kingdom of Cambodia. National Route 13 streches towards border to Cambodia. So the answer is: Cambodia.
New answer: FINISH[Cambodia]

Question: Jeremy Theobald and Christopher Nolan share what profession?
Old answer: Jeremy Theobald is an actor and producer. Christopher Nolan is a director, producer, and screenwriter. Therefore, they both share the profession of being a producer. So the answer is: producer.
New answer: FINISH[producer]
'''.strip()

answer_format_prompt = f"{answer_format_instructions}\n\n" + f"Here are some examples:\n{answer_format_examples}\n\n" + '''
Question: {question}
Old answer: {answer}
New answer:
'''.strip()
