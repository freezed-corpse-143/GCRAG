from concurrent.futures import ThreadPoolExecutor, as_completed
from .llm_filter import ground_step

def tournament_filter(examples, question, retrieved_documents,
                     thought, answer, batch_size=3):
    
    prev_supporting_docs = retrieved_documents.copy()
    prev_supporting_ids = [doc['id'] for doc in prev_supporting_docs]
    current_supporting_docs = []
    current_supporting_ids = []
    final_answer = None
    
    while True:
        current_supporting_docs = []
        current_supporting_ids = []

        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = []
            for i in range(0, len(prev_supporting_docs), batch_size):
                batch = prev_supporting_docs[i:i+batch_size]
                futures.append(
                    executor.submit(
                        ground_step,
                        examples=examples,
                        question=question,
                        retrieved_documents=batch,
                        thought=thought,
                        answer=answer
                    )
                )
            
            # Process results as they complete
            for future in as_completed(futures):
                try:
                    new_answer, new_supporting_docs, new_supporting_ids = future.result()
                    if new_supporting_ids:
                        final_answer = new_answer
                        for id, doc in zip(new_supporting_ids, new_supporting_docs):
                            if id not in current_supporting_ids:
                                current_supporting_docs.append(doc)
                                current_supporting_ids.append(id)
                except Exception as e:
                    print(f"Error processing batch: {e}")
                    continue
        
        
        if set(current_supporting_ids) == set(prev_supporting_ids):
            break
            
        prev_supporting_docs = current_supporting_docs.copy()
        prev_supporting_ids = current_supporting_ids.copy()
    return final_answer, current_supporting_docs, current_supporting_ids