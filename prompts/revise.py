
revise_prompt = '''
Original question:
{original_question}

Previous hypothesis:
{current_hypothesis}

Subquestion:
{subquestion}

Retrieved documents:
{retrieved_documents}

Based on this information, refine the hypothesis to better answer the original question.
Return ONLY the refined hypothesis without any additional text.
'''.strip()