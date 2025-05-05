decompose_prompt = '''
{instructions}

Here are some examples of how to answer step-by-step:
{examples}

Now answer the following question using the same format:
Input:
Question: {question}
{thoughts_and_answers}
New one thought/answer pair:
'''.strip()


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
