from prompts.template import ground_prompt
from .utils import format_retr_docs, generate, extract_from_ground_answer

def ground_step(examples, question, retrieved_documents,
                thought, answer):
    prompt = ground_prompt.format(
        examples=examples,
        question=question,
        retrieved_documents=format_retr_docs(retrieved_documents),
        thought=thought,
        answer=answer,
    ).strip()

    answer_ok = False
    new_answer = ""
    sp_fact_ids = []
    retr_len = len(retrieved_documents)
    while not answer_ok:
        generated_result = generate(prompt)
        generated_text = generated_result['generated_text'].strip()
        
        if "New answer" not in generated_text or "Supporting fact ids" not in generated_text:
            prompt += "."
            continue
        new_answer, sp_fact_ids = extract_from_ground_answer(generated_text)
        answer_ok = True
    current_supporting_docs = []
    current_supporting_ids = []
    if sp_fact_ids:
        for item in sp_fact_ids:
            if item <= retr_len:
                document = retrieved_documents[item-1]
                current_supporting_docs.append(document)
                current_supporting_ids.append(document['id'])
    return new_answer, current_supporting_docs, current_supporting_ids
