from prompts.GenGround import (
    ground_prompt,
    ground_examples_prompt,
    ground_single_prompt,
    ground_single_examples,
)

from utils.string import (
    extract_from_ground_answer,
    format_retr_docs,
)

from utils.serve import generate
from metrics.evaluate import single_f1_score

import copy
from collections import defaultdict
import random

random.seed(42)

def ground_step(question, retrieved_documents,
                thought, answer, top_k=1, shuffle_times=3):
    if len(retrieved_documents) == 0:
        return "", []
    # Initialize a dictionary to store the total scores for each document
    total_scores = defaultdict(float)
    for _ in range(shuffle_times):
        # Shuffle the retrieved documents
        random.shuffle(retrieved_documents)
        
        prompt = ground_prompt.format(
            examples=ground_examples_prompt,
            question=question,
            retrieved_documents=format_retr_docs(retrieved_documents),
            thought=thought,
            answer=answer,
        ).strip()
        
        new_answer = answer
        try:
            while True:
                generated_text = generate(prompt)['generated_text'].strip()
                
                # if "New answer" not in generated_text:
                #     prompt += ". Please generate \"New answer:\" as a prefix."
                #     continue
                
                new_answer = extract_from_ground_answer(generated_text)
                if new_answer:
                    break
                prompt += ". Please generate \"New answer:\" as a prefix."
            # Calculate the F1 score for each document
            scores = single_f1_score(new_answer, [item["paragraph_text"] for item in retrieved_documents])
            
            # Accumulate the scores for each document
            for doc, score in zip(retrieved_documents, scores):
                total_scores[doc['id']] += score
        
        except Exception as e:
            print(e)
    
    # Sort the documents by their total scores in descending order
    sorted_docs = sorted(total_scores.items(), key=lambda x: x[1], reverse=True)
    
    # Return the top_k documents and the new answer
    top_k_ids = [doc_id for doc_id, _ in sorted_docs[:top_k]]
    top_k_docs = [doc for doc in retrieved_documents if doc['id'] in top_k_ids]
    return new_answer, top_k_docs

def batch_ground_step(
        question, retrieved_documents,
        thought, answer, batch_size=10, 
        top_k=2, shuffle_times=3):
    tmp = copy.deepcopy(retrieved_documents)

    temp_answer = answer
    while len(tmp) >= batch_size:
        temp_answer, docs = ground_step(
            question=question,
            retrieved_documents=tmp[:batch_size],
            thought=thought,
            answer=answer,
            top_k=top_k,
            shuffle_times=shuffle_times,
        )
        tmp = tmp[batch_size:]+docs
    # new_answer, _ = ground_step(
    #     examples=examples,
    #     question=question,
    #     retrieved_documents=tmp,
    #     thought=thought,
    #     answer=answer,
    # )
    return temp_answer, tmp
    

def ground_single(question, 
                  thought,
                  retrieved_documents,):
    result_docs = []
    result_ids = []
    for doc in retrieved_documents:
        prompt = ground_single_prompt.format(
            examples = ground_single_examples,
            question = question,
            thought = thought,
            document = doc['paragraph_text'],
        )
        while True:
            generated_text = generate(prompt, stop=[' ', '\n', '.'])['generated_text'].strip().lower()
            if "true" in generated_text and doc['id'] not in result_ids:
                result_ids.append(doc['id'])
                result_docs.append(doc)
                break
            if 'false' in generated_text:
                break
            prompt += '.'
    return result_docs, result_ids

