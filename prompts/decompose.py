
decompose_prompt = '''
Original question:
{original_question}

Current hypothesis:
{current_hypothesis}

Decompose this into a single subquestion that would help verify or refine the hypothesis.
Return ONLY the subquestion without any additional text.
'''.strip()