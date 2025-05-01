import jsonlines
import json
import os
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed

def process_row(row):
    """Process a single row from the Musique dataset."""
    return {
        "id": row["id"],
        "question": row["question"],
        "answer": [row["answer"]] + row['answer_aliases'],
        "context": [{
            "title": item['title'], 
            "content": item["paragraph_text"].strip().replace('\xa0', ' ').replace("  ", " "),
            "is_supporting": item['is_supporting'], }
            for item in row["paragraphs"]],
        'question_decomposition': row['question_decomposition'],
        'answerable': row['answerable'],
    }
def format_musique(input_path, output_path, max_workers=12):
    """Process Musique dataset with parallel processing and unified writing."""
    # Read all data first (using jsonlines)
    with jsonlines.open(input_path, mode="r") as reader:
        data = list(reader)
    
    # Process rows in parallel
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(process_row, row) for row in data]
        
        # Write results as they become available
        with open(output_path, "w", encoding="utf-8") as f:
            for future in tqdm(as_completed(futures), total=len(data)):
                processed_item = future.result()
                f.write(json.dumps(processed_item, ensure_ascii=False) + "\n")

if __name__  == "__main__":
    os.makedirs("./datasets/musique", exist_ok=True)
    format_musique("./download/musique/musique_ans_v1.0_train.jsonl", 
                   "./datasets/musique/train.jsonl")
    format_musique("./download/musique/musique_ans_v1.0_dev.jsonl", 
                   "./datasets/musique/dev.jsonl")